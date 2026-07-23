"""
Application service registration.
"""

from __future__ import annotations

from app.application.ai.services.ai_execution_service import (
    AIExecutionService,
)

from app.application.ai.ports import AIProvider


def ai_execution_service(
    provider: AIProvider,
) -> AIExecutionService:
    """
    Create AIExecutionService.
    """

    return AIExecutionService(
        provider,
    )