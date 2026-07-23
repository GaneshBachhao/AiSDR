from app.domain.ai.aggregates.ai_request import AIRequest
from app.domain.ai.entities.ai_response import AIResponse
from ..clients.openai_client import OpenAIClient
from ..configuration import ProviderSettings
from ..exceptions.ai_provider_exception import AIProviderException

from .base_provider import BaseAIProvider


class OpenAIProvider(BaseAIProvider):
    """
    OpenAI provider implementation.
    """


    def __init__(
        self,
        client: OpenAIClient,
        settings: ProviderSettings,
    ):
        self._client = client
        self._settings = settings


    async def execute(
        self,
        request: AIRequest,
    ) -> AIResponse:
        """
        Execute request using OpenAI.
        """

        try:
            payload = {
                "model": request.model.value,
                "messages": request.messages,
                "temperature": request.temperature,
                "max_tokens": request.max_tokens,
            }

            response = await self._client.send_request(
                payload
            )

            # Adapter integration will be added here.
            #
            # return AIResponseAdapter.from_openai(
            #     response
            # )

            return response

        except Exception as exc:
            raise AIProviderException(
                "OpenAI provider execution failed"
            ) from exc


    async def health_check(self) -> bool:
        """
        Check OpenAI availability.
        """

        return await self._client.health_check()