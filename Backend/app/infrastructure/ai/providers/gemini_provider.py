from app.domain.ai.aggregates.ai_request import AIRequest
from app.domain.ai.entities.ai_response import AIResponse
from app.domain.ai.enums.finish_reason import FinishReason
from app.domain.ai.value_objects.token_usage import TokenUsage

from ..clients.gemini_client import GeminiClient
from ..configuration import ProviderSettings
from ..exceptions.ai_provider_exception import AIProviderException
from .base_provider import BaseAIProvider

_FINISH_REASON_MAP = {
    "STOP": FinishReason.STOP,
    "MAX_TOKENS": FinishReason.LENGTH,
    "SAFETY": FinishReason.CONTENT_FILTER,
    "PROHIBITED_CONTENT": FinishReason.CONTENT_FILTER,
    "BLOCKLIST": FinishReason.CONTENT_FILTER,
    "SPII": FinishReason.CONTENT_FILTER,
}


class GeminiProvider(BaseAIProvider):
    """
    Google Gemini provider implementation.
    """

    def __init__(
        self,
        client: GeminiClient,
        settings: ProviderSettings,
    ):
        self._client = client
        self._settings = settings

    async def execute(
        self,
        request: AIRequest,
    ) -> AIResponse:
        """
        Execute request using Gemini.
        """

        try:
            payload = {
                "model": request.model.value,
                "contents": request.prompt.value,
                "temperature": request.temperature.value,
                "max_tokens": request.max_tokens.value,
            }

            raw_response = await self._client.send_request(payload)

            return AIResponse(
                content=raw_response["content"],
                finish_reason=_FINISH_REASON_MAP.get(
                    raw_response.get("finish_reason", "STOP"),
                    FinishReason.STOP,
                ),
                token_usage=TokenUsage(
                    prompt_tokens=raw_response.get("prompt_tokens", 0),
                    completion_tokens=raw_response.get("completion_tokens", 0),
                ),
            )

        except Exception as exc:
            raise AIProviderException("Gemini provider execution failed") from exc

    async def health_check(self) -> bool:
        """
        Check Gemini availability.
        """

        return await self._client.health_check()
