from app.domain.ai.aggregates.ai_request import AIRequest
from app.domain.ai.entities.ai_response import AIResponse

from ..clients.gemini_client import GeminiClient
from ..configuration import ProviderSettings
from ..exceptions.ai_provider_exception import AIProviderException

from .base_provider import BaseAIProvider


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
                "contents": request.messages,
                "temperature": request.temperature,
                "max_tokens": request.max_tokens,
            }


            response = await self._client.send_request(
                payload
            )


            # Future:
            #
            # return AIResponseAdapter.from_gemini(
            #     response
            # )


            return response


        except Exception as exc:

            raise AIProviderException(
                "Gemini provider execution failed"
            ) from exc


    async def health_check(self) -> bool:
        """
        Check Gemini availability.
        """

        return await self._client.health_check()