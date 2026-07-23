"""
Infrastructure adapter implementing the
Application AIProvider port.
"""

from __future__ import annotations

from app.application.ai.ports import AIProvider

from app.domain.ai.aggregates.ai_request import AIRequest
from app.domain.ai.entities.ai_response import AIResponse

from app.infrastructure.ai.factories import AIProviderFactory


class ApplicationAIProvider(AIProvider):
    """
    Bridges the Application layer and
    Infrastructure provider implementations.
    """

    def __init__(
        self,
        provider_factory: AIProviderFactory,
    ) -> None:
        self._provider_factory = provider_factory

    async def execute(
        self,
        request: AIRequest,
    ) -> AIResponse:

        provider = self._provider_factory.create(
            request.provider.value,
        )

        return await provider.execute(
            request,
        )