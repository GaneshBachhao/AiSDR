"""
Application port for recording AI provider usage.

Decouples ``AIExecutionService`` from any specific persistence mechanism
for usage/cost tracking. Implementations live in the infrastructure layer.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.ai.aggregates.ai_request import AIRequest


class AIUsageRecorder(ABC):
    """Application port for logging a completed or failed AI call."""

    @abstractmethod
    async def log(
        self,
        request: AIRequest,
    ) -> None:
        """Record usage for one AI request. Must never raise."""
        raise NotImplementedError
