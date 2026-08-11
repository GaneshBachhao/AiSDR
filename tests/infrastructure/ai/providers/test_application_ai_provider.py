from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from app.domain.ai.aggregates.ai_request import AIRequest
from app.domain.ai.entities.ai_response import AIResponse
from app.domain.ai.enums.finish_reason import FinishReason
from app.domain.ai.value_objects.max_tokens import MaxTokens
from app.domain.ai.value_objects.model_name import ModelName
from app.domain.ai.value_objects.prompt import Prompt
from app.domain.ai.value_objects.provider_name import ProviderName
from app.domain.ai.value_objects.temperature import Temperature
from app.domain.ai.value_objects.token_usage import TokenUsage
from app.infrastructure.ai.adapters import ApplicationAIProvider


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
        content="Architecture explained.",
        finish_reason=FinishReason.STOP,
        token_usage=TokenUsage(prompt_tokens=10, completion_tokens=20),
    )


def create_provider():
    infrastructure_provider = AsyncMock()
    infrastructure_provider.execute.return_value = create_response()
    infrastructure_provider.health_check.return_value = True
    provider = ApplicationAIProvider(providers={"gemini": infrastructure_provider})
    return provider, infrastructure_provider


@pytest.mark.asyncio
async def test_execute_returns_response():
    provider, infra = create_provider()
    result = await provider.execute(create_request())
    assert isinstance(result, AIResponse)


@pytest.mark.asyncio
async def test_provider_execute_called_once():
    provider, infra = create_provider()
    request = create_request()
    await provider.execute(request)
    infra.execute.assert_awaited_once_with(request)


@pytest.mark.asyncio
async def test_response_content():
    provider, _ = create_provider()
    response = await provider.execute(create_request())
    assert response.content == "Architecture explained."


@pytest.mark.asyncio
async def test_finish_reason_and_token_usage():
    provider, _ = create_provider()
    response = await provider.execute(create_request())
    assert response.finish_reason == FinishReason.STOP
    assert response.token_usage.total_tokens == 30


@pytest.mark.asyncio
async def test_unsupported_provider_raises():
    provider = ApplicationAIProvider(providers={})
    with pytest.raises(ValueError, match="Unsupported AI provider"):
        await provider.execute(create_request())


@pytest.mark.asyncio
async def test_provider_exception_propagates():
    infra = AsyncMock()
    infra.execute.side_effect = RuntimeError("Execution failed.")
    provider = ApplicationAIProvider(providers={"gemini": infra})
    with pytest.raises(RuntimeError, match="Execution failed"):
        await provider.execute(create_request())


@pytest.mark.asyncio
async def test_health_check():
    provider, _ = create_provider()
    assert await provider.health_check("gemini") is True
    assert await provider.health_check("missing") is False
