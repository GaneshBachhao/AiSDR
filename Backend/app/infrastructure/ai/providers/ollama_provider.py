"""
Ollama AI provider.
"""

from __future__ import annotations

from app.domain.ai.aggregates.ai_request import AIRequest
from app.domain.ai.entities.ai_response import AIResponse

from .base_provider import BaseAIProvider


class OllamaProvider(BaseAIProvider):
    """
    Ollama implementation.

    Placeholder until HTTP execution
    is implemented.
    """

    def __init__(
        self,
        client,
        settings,
    ) -> None:
        self._client = client
        self._settings = settings

    async def execute(
        self,
        request: AIRequest,
    ) -> AIResponse:
        raise NotImplementedError("Ollama provider not implemented.")

    async def health_check(
        self,
    ) -> bool:
        return False
