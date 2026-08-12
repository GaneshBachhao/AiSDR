"""
Tests for AIExecutionService.
"""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from app.application.ai.ports import AIProvider
from app.application.ai.services.ai_execution_service import (
    AIExecutionService,
)
from app.domain.ai.aggregates.ai_request import AIRequest
from app.domain.ai.entities.ai_response import AIResponse
from app.domain.ai.enums.ai_request_status import AIRequestStatus
from app.domain.ai.enums.finish_reason import FinishReason
from app.domain.ai.value_objects.max_tokens import MaxTokens
from app.domain.ai.value_objects.model_name import ModelName
from app.domain.ai.value_objects.prompt import Prompt
from app.domain.ai.value_objects.provider_name import ProviderName
from app.domain.ai.value_objects.temperature import Temperature
from app.domain.ai.value_objects.token_usage import TokenUsage


# ==========================================================
# Helpers
# ==========================================================

def create_request() -> AIRequest:
    return AIRequest(
        provider=ProviderName("gemini"),
        model=ModelName("gemini-2.5-pro"),
        prompt=Prompt("Explain Clean Architecture."),
        temperature=Temperature(0.7),
        max_tokens=MaxTokens(1024),
    )


def create_response() -> AIResponse:
    return AIResponse(
        content="Architecture explanation.",
        finish_reason=FinishReason.STOP,
        token_usage=TokenUsage(
            prompt_tokens=10,
            completion_tokens=20,
        ),
    )


# ==========================================================
# Happy Path
# ==========================================================

@pytest.mark.asyncio
async def test_execute_returns_response() -> None:
    provider = AsyncMock(spec=AIProvider)

    response = create_response()

    provider.execute.return_value = response

    service = AIExecutionService(provider)

    request = create_request()

    result = await service.execute(request)

    assert result == response


@pytest.mark.asyncio
async def test_execute_starts_request() -> None:
    provider = AsyncMock(spec=AIProvider)

    provider.execute.return_value = create_response()

    service = AIExecutionService(provider)

    request = create_request()

    await service.execute(request)

    assert request.started_at is not None
    assert request.status == AIRequestStatus.COMPLETED


@pytest.mark.asyncio
async def test_execute_completes_request() -> None:
    provider = AsyncMock(spec=AIProvider)

    response = create_response()

    provider.execute.return_value = response

    service = AIExecutionService(provider)

    request = create_request()

    await service.execute(request)

    assert request.response == response
    assert request.completed_at is not None
    assert request.is_completed


@pytest.mark.asyncio
async def test_provider_called_once() -> None:
    provider = AsyncMock(spec=AIProvider)

    provider.execute.return_value = create_response()

    service = AIExecutionService(provider)

    request = create_request()

    await service.execute(request)

    provider.execute.assert_awaited_once_with(request)


# ==========================================================
# Failure
# ==========================================================

@pytest.mark.asyncio
async def test_execute_marks_request_failed() -> None:
    provider = AsyncMock(spec=AIProvider)

    provider.execute.side_effect = RuntimeError(
        "Provider unavailable."
    )

    service = AIExecutionService(provider)

    request = create_request()

    with pytest.raises(RuntimeError):

        await service.execute(request)

    assert request.is_failed
    assert request.failure_reason == "Provider unavailable."
    assert request.completed_at is not None


@pytest.mark.asyncio
async def test_execute_propagates_exception() -> None:
    provider = AsyncMock(spec=AIProvider)

    provider.execute.side_effect = RuntimeError(
        "Boom"
    )

    service = AIExecutionService(provider)

    request = create_request()

    with pytest.raises(RuntimeError):

        await service.execute(request)


@pytest.mark.asyncio
async def test_failed_request_status() -> None:
    provider = AsyncMock(spec=AIProvider)

    provider.execute.side_effect = RuntimeError(
        "Failure"
    )

    service = AIExecutionService(provider)

    request = create_request()

    with pytest.raises(RuntimeError):

        await service.execute(request)

    assert request.status == AIRequestStatus.FAILED


@pytest.mark.asyncio
async def test_response_is_attached_to_request() -> None:
    provider = AsyncMock(spec=AIProvider)

    response = create_response()

    provider.execute.return_value = response

    service = AIExecutionService(provider)

    request = create_request()

    await service.execute(request)

    assert request.response is response


@pytest.mark.asyncio
async def test_health_check_all_delegates_to_provider() -> None:
    provider = AsyncMock(spec=AIProvider)
    provider.health_check_all.return_value = {"gemini": True, "openai": False}

    service = AIExecutionService(provider)

    result = await service.health_check_all()

    assert result == {"gemini": True, "openai": False}
    provider.health_check_all.assert_awaited_once()