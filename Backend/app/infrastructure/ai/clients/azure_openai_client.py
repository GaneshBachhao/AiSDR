from __future__ import annotations

from typing import Any

from ..configuration import ProviderSettings
from ..exceptions.ai_client_exception import AIClientException
from .base_ai_client import BaseAIClient

try:
    from openai import AsyncAzureOpenAI
except ImportError:  # optional integration dependency
    AsyncAzureOpenAI = None


class AzureOpenAIClient(BaseAIClient):
    """
    Infrastructure client for Azure OpenAI communication.

    ``payload["model"]``/``payload["deployment"]`` must be the Azure
    *deployment* name configured in the Azure OpenAI resource -- Azure
    routes requests by deployment, not by base model family.
    """

    def __init__(
        self,
        settings: ProviderSettings,
    ):
        self._settings = settings
        self._sdk_installed = AsyncAzureOpenAI is not None
        self._configured = bool(settings.api_key and settings.endpoint and settings.api_version)
        self._client = (
            AsyncAzureOpenAI(
                api_key=settings.api_key,
                azure_endpoint=settings.endpoint,
                api_version=settings.api_version,
            )
            if self._sdk_installed and self._configured
            else None
        )

    async def send_request(
        self,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Send request to the Azure OpenAI API.

        Returns a raw response dict with ``content``, ``finish_reason``,
        ``prompt_tokens`` and ``completion_tokens`` keys.
        """

        if not self._sdk_installed:
            raise AIClientException("Azure OpenAI request failed: the 'openai' package is not installed.")

        if self._client is None:
            raise AIClientException(
                "Azure OpenAI request failed: endpoint, API key, and API version must all be configured."
            )

        try:
            deployment = str(payload.get("deployment") or payload["model"])
            response = await self._client.chat.completions.create(
                model=deployment,
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
            raise AIClientException("Azure OpenAI request failed") from exc

    async def health_check(self) -> bool:
        """
        Verify Azure OpenAI availability.
        """

        return self._sdk_installed and self._client is not None
