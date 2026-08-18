"""
Tests for ExecuteAIRequestHandler.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, Mock

import pytest

from app.application.ai.commands.execute_ai_request import (
    ExecuteAIRequestCommand,
)
from app.application.ai.dto.ai_response_dto import (
    AIResponseDTO,
)
from app.application.ai.handlers.execute_ai_request_handler import (
    ExecuteAIRequestHandler,
)
from app.application.common.handler.handler_context import (
    HandlerContext,
)
from app.domain.ai.entities.ai_response import (
    AIResponse,
)
from app.domain.ai.enums.finish_reason import (
    FinishReason,
)
from app.domain.ai.value_objects.token_usage import (
    TokenUsage,
)

# ==========================================================
# Helpers
# ==========================================================


def create_command() -> ExecuteAIRequestCommand:
    return ExecuteAIRequestCommand(
        provider="gemini",
        model="gemini-2.5-pro",
        prompt="Explain Clean Architecture.",
        temperature=0.7,
        max_tokens=1024,
    )


def create_response() -> AIResponse:
    return AIResponse(
        content="Architecture explained.",
        finish_reason=FinishReason.STOP,
        token_usage=TokenUsage(
            prompt_tokens=10,
            completion_tokens=20,
        ),
    )


def create_handler():

    repository = AsyncMock()

    execution_service = AsyncMock()

    validation_service = Mock()

    handler = ExecuteAIRequestHandler(
        repository=repository,
        execution_service=execution_service,
        validation_service=validation_service,
    )

    return (
        handler,
        repository,
        execution_service,
        validation_service,
    )


# ==========================================================
# Happy Path
# ==========================================================


@pytest.mark.asyncio
async def test_handle_success():

    (
        handler,
        repository,
        execution_service,
        validation_service,
    ) = create_handler()

    command = create_command()

    response = create_response()

    execution_service.execute.return_value = response

    context = HandlerContext()

    result = await handler.handle(
        command,
        context,
    )

    validation_service.validate.assert_called_once()

    execution_service.execute.assert_awaited_once()

    repository.save.assert_awaited_once()

    assert result.is_success
    assert isinstance(
        result.data,
        AIResponseDTO,
    )

    assert result.message == "AI request executed successfully."


# ==========================================================
# Validation Failure
# ==========================================================


@pytest.mark.asyncio
async def test_handle_validation_failure():

    (
        handler,
        repository,
        execution_service,
        validation_service,
    ) = create_handler()

    command = create_command().model_copy(
        update={
            "provider": " ",
        }
    )

    context = HandlerContext()

    result = await handler.handle(
        command,
        context,
    )

    assert not result.is_success

    execution_service.execute.assert_not_called()

    repository.save.assert_not_called()


# ==========================================================
# Validation Service
# ==========================================================


@pytest.mark.asyncio
async def test_validation_service_called():

    (
        handler,
        repository,
        execution_service,
        validation_service,
    ) = create_handler()

    execution_service.execute.return_value = create_response()

    await handler.handle(
        create_command(),
        HandlerContext(),
    )

    validation_service.validate.assert_called_once()


# ==========================================================
# Repository
# ==========================================================


@pytest.mark.asyncio
async def test_repository_save_called():

    (
        handler,
        repository,
        execution_service,
        validation_service,
    ) = create_handler()

    execution_service.execute.return_value = create_response()

    await handler.handle(
        create_command(),
        HandlerContext(),
    )

    repository.save.assert_awaited_once()


# ==========================================================
# Execution Service
# ==========================================================


@pytest.mark.asyncio
async def test_execution_service_called():

    (
        handler,
        repository,
        execution_service,
        validation_service,
    ) = create_handler()

    execution_service.execute.return_value = create_response()

    await handler.handle(
        create_command(),
        HandlerContext(),
    )

    execution_service.execute.assert_awaited_once()


# ==========================================================
# Response DTO
# ==========================================================


@pytest.mark.asyncio
async def test_response_dto_returned():

    (
        handler,
        repository,
        execution_service,
        validation_service,
    ) = create_handler()

    execution_service.execute.return_value = create_response()

    result = await handler.handle(
        create_command(),
        HandlerContext(),
    )

    assert isinstance(
        result.data,
        AIResponseDTO,
    )


# ==========================================================
# No Response
# ==========================================================


@pytest.mark.asyncio
async def test_handle_without_response():

    (
        handler,
        repository,
        execution_service,
        validation_service,
    ) = create_handler()

    execution_service.execute.return_value = None

    result = await handler.handle(
        create_command(),
        HandlerContext(),
    )

    assert not result.is_success

    assert result.message == "AI request completed without response."


# ==========================================================
# Execution Exception
# ==========================================================


@pytest.mark.asyncio
async def test_execution_exception_propagates():

    (
        handler,
        repository,
        execution_service,
        validation_service,
    ) = create_handler()

    execution_service.execute.side_effect = RuntimeError("Execution failed.")

    with pytest.raises(RuntimeError):
        await handler.handle(
            create_command(),
            HandlerContext(),
        )


# ==========================================================
# Success Message
# ==========================================================


@pytest.mark.asyncio
async def test_success_message():

    (
        handler,
        repository,
        execution_service,
        validation_service,
    ) = create_handler()

    execution_service.execute.return_value = create_response()

    result = await handler.handle(
        create_command(),
        HandlerContext(),
    )

    assert result.message == "AI request executed successfully."


# ==========================================================
# Returned Content
# ==========================================================


@pytest.mark.asyncio
async def test_returned_content():

    (
        handler,
        repository,
        execution_service,
        validation_service,
    ) = create_handler()

    execution_service.execute.return_value = create_response()

    result = await handler.handle(
        create_command(),
        HandlerContext(),
    )

    assert result.data.content == "Architecture explained."
