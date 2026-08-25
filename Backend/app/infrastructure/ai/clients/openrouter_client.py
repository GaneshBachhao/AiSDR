"""OpenRouter client -- reuses the ``openai`` SDK (OpenRouter is designed as
a drop-in replacement for the same API surface: same ``AsyncOpenAI`` client,
just a different ``base_url`` and key), kept as its own class rather than a
configurable ``OpenAIClient`` so "OpenAI the paid provider" (excluded) stays
structurally distinct from "OpenRouter the aggregator" (the one deliberate
exception -- see AI_PROVIDER_FALLBACK's comment in .env).

Unlike ``OpenAIClient``/``AzureOpenAIClient`` (neither of which currently
detects a 429), this client raises ``AIRateLimitException`` on one -- the
whole point of adding OpenRouter is to fail over here when Gemini is
rate-limited, so a rate-limited OpenRouter response needs to be visibly
distinct from a real failure, same discipline as ``GeminiClient``.
"""

from __future__ import annotations

from typing import Any

from ..configuration import ProviderSettings
from ..exceptions.ai_client_exception import AIClientException
from ..exceptions.ai_rate_limit_exception import AIRateLimitException
from .base_ai_client import BaseAIClient

try:
    from openai import AsyncOpenAI, RateLimitError
except ImportError:  # optional integration dependency
    AsyncOpenAI = None
    RateLimitError = None


def _retry_after_seconds(exc: Any) -> float | None:
    """Best-effort extraction of a Retry-After header. Never raises -- an
    unexpected response shape just means no retry hint, not a broken
    rate-limit detection (mirrors GeminiClient's identical helper)."""
    try:
        value = exc.response.headers.get("retry-after")
        return float(value) if value is not None else None
    except Exception:
        return None


class OpenRouterClient(BaseAIClient):
    """
    Infrastructure client for OpenRouter communication.
    """

    def __init__(
        self,
        settings: ProviderSettings,
    ):
        self._settings = settings
        self._sdk_installed = AsyncOpenAI is not None
        self._client = (
            AsyncOpenAI(api_key=settings.api_key, base_url=settings.endpoint)
            if self._sdk_installed and settings.api_key
            else None
        )

    async def send_request(
        self,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        if not self._sdk_installed:
            raise AIClientException("OpenRouter request failed: the 'openai' package is not installed.")

        if self._client is None:
            raise AIClientException("OpenRouter request failed: no API key is configured.")

        try:
            response = await self._client.chat.completions.create(
                model=str(payload["model"]),
                messages=[{"role": "user", "content": str(payload["contents"])}],
                temperature=payload.get("temperature"),
                max_tokens=payload.get("max_tokens"),
            )

            choice = response.choices[0]
            usage = response.usage

            return {
                "content": choice.message.content or "",
                "finish_reason": choice.finish_reason or "stop",
                "prompt_tokens": (usage.prompt_tokens if usage else 0) or 0,
                "completion_tokens": (usage.completion_tokens if usage else 0) or 0,
            }

        except AIClientException:
            raise
        except Exception as exc:
            if RateLimitError is not None and isinstance(exc, RateLimitError):
                raise AIRateLimitException(
                    f"OpenRouter rate limit / quota exceeded: {exc}",
                    retry_after_seconds=_retry_after_seconds(exc),
                ) from exc
            raise AIClientException("OpenRouter request failed") from exc

    async def health_check(self) -> bool:
        return self._sdk_installed and self._client is not None
