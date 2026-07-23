"""
Command handler registration.
"""

from __future__ import annotations

from app.application.ai.handlers.execute_ai_request_handler import (
    ExecuteAIRequestHandler,
)

from app.application.ai.services.ai_execution_service import (
    AIExecutionService,
)

from app.application.ai.validators.execute_ai_request_validator import (
    ExecuteAIRequestValidator,
)


def execute_ai_request_handler(
    service: AIExecutionService,
) -> ExecuteAIRequestHandler:
    """
    Create ExecuteAIRequestHandler.
    """

    return ExecuteAIRequestHandler(
        service=service,
        validator=ExecuteAIRequestValidator(),
    )