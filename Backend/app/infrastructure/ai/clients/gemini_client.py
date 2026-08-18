from __future__ import annotations

import logging
from typing import Any

from ..configuration import ProviderSettings
from ..exceptions.ai_client_exception import AIClientException
from ..exceptions.ai_rate_limit_exception import AIRateLimitException
from .base_ai_client import BaseAIClient

try:
    from google import genai
    from google.genai import errors as genai_errors
    from google.genai import types as genai_types
except ImportError:  # optional integration dependency
    genai = None
    genai_errors = None
    genai_types = None

logger = logging.getLogger(__name__)


def _retry_after_seconds(exc: genai_errors.ClientError) -> float | None:
    """Best-effort extraction of the server-suggested retry delay from a
    Gemini 429 error body (``{"error": {"details": [{"@type": "...RetryInfo",
    "retryDelay": "14s"}, ...]}}``). Never raises -- an unexpected error
    shape just means no retry hint, not a broken rate-limit detection."""
    try:
        details = exc.details or {}
        error_body = details.get("error", details)
        for entry in error_body.get("details", []):
            delay = entry.get("retryDelay")
            if isinstance(delay, str) and delay.endswith("s"):
                return float(delay[:-1])
    except Exception:
        return None
    return None


class GeminiClient(BaseAIClient):
    """
    Infrastructure client for Google Gemini API communication.
    """

    def __init__(
        self,
        settings: ProviderSettings,
    ):
        self._settings = settings
        self._sdk_installed = genai is not None
        self._client = (
            genai.Client(api_key=settings.api_key) if self._sdk_installed and settings.api_key else None
        )

    async def send_request(
        self,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Send request to the Gemini API.

        Returns a raw response dict with ``content``, ``finish_reason``,
        ``prompt_tokens`` and ``completion_tokens`` keys.
        """

        if not self._sdk_installed:
            raise AIClientException("Gemini request failed: the 'google-genai' package is not installed.")

        if self._client is None:
            raise AIClientException("Gemini request failed: no API key is configured.")

        try:
            config = genai_types.GenerateContentConfig(
                temperature=payload.get("temperature"),
                max_output_tokens=payload.get("max_tokens"),
                # AIResponse has no field for model "thoughts" -- this client models a
                # plain single-turn completion, so thinking tokens (which otherwise
                # silently consume max_output_tokens and can truncate the visible
                # answer) are disabled rather than exposed as part of the contract.
                thinking_config=genai_types.ThinkingConfig(thinking_budget=0),
            )

            response = await self._client.aio.models.generate_content(
                model=str(payload["model"]),
                contents=str(payload["contents"]),
                config=config,
            )

            usage = response.usage_metadata
            finish_reason = None
            if response.candidates:
                finish_reason = response.candidates[0].finish_reason

            return {
                "content": response.text or "",
                "finish_reason": finish_reason.name if finish_reason else "STOP",
                "prompt_tokens": (usage.prompt_token_count if usage else 0) or 0,
                "completion_tokens": (usage.candidates_token_count if usage else 0) or 0,
            }

        except AIClientException:
            raise
        except Exception as exc:
            if (
                genai_errors is not None
                and isinstance(exc, genai_errors.ClientError)
                and (exc.code == 429 or exc.status == "RESOURCE_EXHAUSTED")
            ):
                retry_after = _retry_after_seconds(exc)
                logger.warning(
                    "RATE_LIMIT gemini status=%s retry_after=%s",
                    exc.status,
                    retry_after,
                )
                raise AIRateLimitException(
                    f"Gemini rate limit / quota exceeded: {exc}",
                    retry_after_seconds=retry_after,
                ) from exc
            raise AIClientException("Gemini request failed") from exc

    async def health_check(self) -> bool:
        """
        Verify Gemini availability.
        """

        return self._sdk_installed and self._client is not None
