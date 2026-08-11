from app.domain.ai.aggregates.ai_request import AIRequest
from app.domain.ai.entities.ai_response import AIResponse

from ..clients.azure_openai_client import AzureOpenAIClient
from ..configuration import ProviderSettings
from ..exceptions.ai_provider_exception import AIProviderException

from .base_provider import BaseAIProvider


class AzureOpenAIProvider(BaseAIProvider):
    """
    Azure OpenAI provider implementation.
    """


    def __init__(
        self,
        client: AzureOpenAIClient,
        settings: ProviderSettings,
    ):
        self._client = client
        self._settings = settings


    async def execute(
        self,
        request: AIRequest,
    ) -> AIResponse:
        """
        Execute request using Azure OpenAI.
        """

        try:
            payload = {
                "deployment": request.model.value,
                "messages": request.messages,
                "temperature": request.temperature,
                "max_tokens": request.max_tokens,
            }

            response = await self._client.send_request(
                payload
            )

            # Final response conversion will be handled by:
            #
            # AIResponseAdapter
            #
            # return AIResponseAdapter.from_azure_openai(
            #     response
            # )

            return response

        except Exception as exc:
            raise AIProviderException(
                "Azure OpenAI provider execution failed"
            ) from exc


    async def health_check(self) -> bool:
        """
        Check Azure OpenAI availability.
        """

        return await self._client.health_check()