# app/application/common/interfaces/ai_provider.py

"""
AI provider application port.

Concrete AI implementations such as OpenAI, Anthropic, local LLMs,
or other providers belong to Infrastructure.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.application.common.dto.ai import (
    AICompletionResponse,
)


class AIProvider(ABC):
    """
    Application contract for AI generation capabilities.
    """

    @abstractmethod
    async def generate(
        self,
        *,
        prompt: str,
        system_instruction: str | None = None,
        model: str | None = None,
    ) -> AICompletionResponse:
        """
        Generate AI content.

        Infrastructure implements provider-specific behavior.
        """
        raise NotImplementedError
