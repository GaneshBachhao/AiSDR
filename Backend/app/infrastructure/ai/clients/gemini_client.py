from __future__ import annotations

from typing import Any

from .base_ai_client import BaseAIClient
from ..configuration import ProviderSettings
from ..exceptions.ai_client_exception import AIClientException

try:
    from google import genai
    from google.genai import types as genai_types
except ImportError:  # optional integration dependency
    genai = None
    genai_types = None


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
            genai.Client(api_key=settings.api_key)
            if self._sdk_installed and settings.api_key
            else None
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
            raise AIClientException(
                "Gemini request failed: the 'google-genai' package is not installed."
            )

        if self._client is None:
            raise AIClientException(
                "Gemini request failed: no API key is configured."
            )

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
            raise AIClientException(
                "Gemini request failed"
            ) from exc

    async def health_check(self) -> bool:
        """
        Verify Gemini availability.
        """

        return self._sdk_installed and self._client is not None
