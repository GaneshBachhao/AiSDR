"""
Infrastructure adapter implementing the
Application AIProvider port.
"""

from __future__ import annotations

from app.application.ai.ports import AIProvider

from app.domain.ai.aggregates.ai_request import AIRequest
from app.domain.ai.entities.ai_response import AIResponse

from app.infrastructure.ai.providers.base_provider import (
    BaseAIProvider,
)


class ApplicationAIProvider(AIProvider):
    """
    Routes AI requests to the configured provider.
    """

    def __init__(
        self,
        providers: dict[str, BaseAIProvider],
    ) -> None:

        self._providers = providers

    async def execute(
        self,
        request: AIRequest,
    ) -> AIResponse:
        """
        Execute request using the selected provider.
        """

        provider_name = request.provider.value.lower()

        provider = self._providers.get(
            provider_name,
        )

        if provider is None:
            raise ValueError(
                f"Unsupported AI provider: {provider_name}"
            )

        return await provider.execute(
            request,
        )

    async def health_check(
        self,
        provider_name: str,
    ) -> bool:
        """
        Check health of a specific provider.
        """

        provider = self._providers.get(
            provider_name.lower(),
        )

        if provider is None:
            return False

        return await provider.health_check()