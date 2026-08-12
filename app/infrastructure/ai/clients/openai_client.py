from __future__ import annotations

from typing import Any

from .base_ai_client import BaseAIClient
from ..configuration import ProviderSettings
from ..exceptions.ai_client_exception import AIClientException

try:
    from openai import AsyncOpenAI
except ImportError:  # optional integration dependency
    AsyncOpenAI = None


class OpenAIClient(BaseAIClient):
    """
    Infrastructure client for OpenAI communication.
    """

    def __init__(
        self,
        settings: ProviderSettings,
    ):
        self._settings = settings
        self._sdk_installed = AsyncOpenAI is not None
        self._client = (
            AsyncOpenAI(api_key=settings.api_key)
            if self._sdk_installed and settings.api_key
            else None
        )

    async def send_request(
        self,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Send request to OpenAI API.

        Returns a raw response dict with ``content``, ``finish_reason``,
        ``prompt_tokens`` and ``completion_tokens`` keys.
        """

        if not self._sdk_installed:
            raise AIClientException(
                "OpenAI request failed: the 'openai' package is not installed."
            )

        if self._client is None:
            raise AIClientException(
                "OpenAI request failed: no API key is configured."
            )

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
            raise AIClientException(
                "OpenAI request failed"
            ) from exc

    async def health_check(self) -> bool:
        """
        Verify OpenAI provider availability.
        """

        return self._sdk_installed and self._client is not None
