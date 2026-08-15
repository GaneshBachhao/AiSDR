from app.domain.ai.aggregates.ai_request import AIRequest
from app.domain.ai.entities.ai_response import AIResponse
from app.domain.ai.value_objects.token_usage import TokenUsage

from ..clients.azure_openai_client import AzureOpenAIClient
from ..configuration import ProviderSettings
from ..exceptions.ai_provider_exception import AIProviderException

from .base_provider import BaseAIProvider
from .openai_finish_reason import map_openai_finish_reason


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
                "contents": request.prompt.value,
                "temperature": request.temperature.value,
                "max_tokens": request.max_tokens.value,
            }

            raw_response = await self._client.send_request(
                payload
            )

            return AIResponse(
                content=raw_response["content"],
                finish_reason=map_openai_finish_reason(
                    raw_response.get("finish_reason", "stop")
                ),
                token_usage=TokenUsage(
                    prompt_tokens=raw_response.get("prompt_tokens", 0),
                    completion_tokens=raw_response.get("completion_tokens", 0),
                ),
            )

        except Exception as exc:
            raise AIProviderException(
                "Azure OpenAI provider execution failed"
            ) from exc


    async def health_check(self) -> bool:
        """
        Check Azure OpenAI availability.
        """

        return await self._client.health_check()