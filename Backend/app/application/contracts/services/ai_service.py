"""
AI service contract.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.ai.aggregates.ai_request import AIRequest
from app.domain.ai.entities.ai_response import AIResponse


class AIService(ABC):
    """
    AI generation service contract.

    Application layer depends on this abstraction.
    Infrastructure provides concrete implementations.
    """

    @abstractmethod
    async def generate(
        self,
        request: AIRequest,
    ) -> AIResponse:
        """
        Generate an AI response from a request.
        """
        raise NotImplementedError