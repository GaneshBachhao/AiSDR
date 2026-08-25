from app.domain.ai.aggregates.ai_request import AIRequest
from app.domain.ai.entities.ai_response import AIResponse
from app.domain.ai.value_objects.token_usage import TokenUsage

from ..clients.openrouter_client import OpenRouterClient
from ..configuration import ProviderSettings
from ..exceptions.ai_provider_exception import AIProviderException
from ..exceptions.ai_rate_limit_exception import AIRateLimitException
from .base_provider import BaseAIProvider
from .openai_finish_reason import map_openai_finish_reason


class OpenRouterProvider(BaseAIProvider):
    """
    OpenRouter provider implementation -- same OpenAI-compatible response
    shape, so it reuses ``map_openai_finish_reason``.
    """

    def __init__(
        self,
        client: OpenRouterClient,
        settings: ProviderSettings,
    ):
        self._client = client
        self._settings = settings

    async def execute(
        self,
        request: AIRequest,
    ) -> AIResponse:
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
                finish_reason=map_openai_finish_reason(raw_response.get("finish_reason", "stop")),
                token_usage=TokenUsage(
                    prompt_tokens=raw_response.get("prompt_tokens", 0),
                    completion_tokens=raw_response.get("completion_tokens", 0),
                ),
            )

        except AIRateLimitException:
            # Preserve type identity, same as GeminiProvider -- callers that
            # special-case a rate limit (fallback loop, adapters) need to
            # see this, not a generic AIProviderException.
            raise
        except Exception as exc:
            raise AIProviderException("OpenRouter provider execution failed") from exc

    async def health_check(self) -> bool:
        return await self._client.health_check()
