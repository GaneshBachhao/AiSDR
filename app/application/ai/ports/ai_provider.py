"""
Application port for AI providers.

This abstraction decouples the application layer from
the infrastructure AI provider implementations.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.ai.aggregates.ai_request import AIRequest
from app.domain.ai.entities.ai_response import AIResponse


class AIProvider(ABC):
    """
    Application port for executing AI requests.
    """

    @abstractmethod
    async def execute(
        self,
        request: AIRequest,
    ) -> AIResponse:
        """
        Execute an AI request and return the response.
        """
        raise NotImplementedError

    @abstractmethod
    async def health_check(
        self,
        provider_name: str,
    ) -> bool:
        """
        Check whether a specific named provider is reachable.
        """
        raise NotImplementedError

    @abstractmethod
    async def health_check_all(
        self,
    ) -> dict[str, bool]:
        """
        Check health of every configured provider.
        """
        raise NotImplementedError