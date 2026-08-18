from datetime import UTC, datetime

from app.domain.ai.aggregates.ai_request import AIRequest
from app.domain.ai.entities.ai_response import AIResponse
from app.domain.ai.enums.finish_reason import FinishReason
from app.domain.ai.value_objects.token_usage import TokenUsage

from ...app.infrastructure.ai.providers.base_provider import BaseAIProvider


class MockProvider(BaseAIProvider):
    """
    Mock AI provider for testing
    and local development.
    """

    async def execute(
        self,
        request: AIRequest,
    ) -> AIResponse:
        """
        Return predictable fake AI response.
        """

        return AIResponse(
            content=("Mock AI response generated successfully."),
            finish_reason=FinishReason.COMPLETED,
            token_usage=TokenUsage(
                prompt_tokens=10,
                completion_tokens=20,
                total_tokens=30,
            ),
            created_at=datetime.now(UTC),
        )

    async def health_check(self) -> bool:
        """
        Mock provider is always available.
        """

        return True
