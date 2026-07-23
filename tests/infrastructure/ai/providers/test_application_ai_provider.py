"""
Tests for ApplicationAIProvider.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, Mock

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

from app.infrastructure.ai.adapters import (
    ApplicationAIProvider,
)
from app.infrastructure.ai.factories import (
    AIProviderFactory,
)



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
        content="Architecture explained.",
        finish_reason=FinishReason.STOP,
        token_usage=TokenUsage(
            prompt_tokens=10,
            completion_tokens=20,
        ),
    )


def create_provider():

    infrastructure_provider = AsyncMock()

    infrastructure_provider.execute.return_value = (
        create_response()
    )

    factory = Mock(
        spec=AIProviderFactory,
    )

    factory.create.return_value = (
        infrastructure_provider
    )

    provider = ApplicationAIProvider(
        provider_factory=factory,
    )

    return (
        provider,
        factory,
        infrastructure_provider,
    )


# ==========================================================
# Execute
# ==========================================================

@pytest.mark.asyncio
async def test_execute_returns_response():

    provider, factory, infra = create_provider()

    request = create_request()

    result = await provider.execute(
        request,
    )

    assert isinstance(
        result,
        AIResponse,
    )


@pytest.mark.asyncio
async def test_factory_called_once():

    provider, factory, infra = create_provider()

    request = create_request()

    await provider.execute(
        request,
    )

    factory.create.assert_called_once_with(
        "gemini",
    )


@pytest.mark.asyncio
async def test_provider_execute_called_once():

    provider, factory, infra = create_provider()

    request = create_request()

    await provider.execute(
        request,
    )

    infra.execute.assert_awaited_once_with(
        request,
    )


@pytest.mark.asyncio
async def test_response_content():

    provider, factory, infra = create_provider()

    request = create_request()

    response = await provider.execute(
        request,
    )

    assert (
        response.content
        == "Architecture explained."
    )


@pytest.mark.asyncio
async def test_finish_reason():

    provider, factory, infra = create_provider()

    request = create_request()

    response = await provider.execute(
        request,
    )

    assert (
        response.finish_reason
        == FinishReason.STOP
    )


@pytest.mark.asyncio
async def test_token_usage():

    provider, factory, infra = create_provider()

    request = create_request()

    response = await provider.execute(
        request,
    )

    assert (
        response.token_usage.total_tokens
        == 30
    )


# ==========================================================
# Exceptions
# ==========================================================

@pytest.mark.asyncio
async def test_factory_exception_propagates():

    factory = Mock(
        spec=AIProviderFactory,
    )

    factory.create.side_effect = RuntimeError(
        "Factory error."
    )

    provider = ApplicationAIProvider(
        provider_factory=factory,
    )

    with pytest.raises(RuntimeError):

        await provider.execute(
            create_request(),
        )


@pytest.mark.asyncio
async def test_provider_exception_propagates():

    infrastructure_provider = AsyncMock()

    infrastructure_provider.execute.side_effect = (
        RuntimeError(
            "Execution failed."
        )
    )

    factory = Mock(
        spec=AIProviderFactory,
    )

    factory.create.return_value = (
        infrastructure_provider
    )

    provider = ApplicationAIProvider(
        provider_factory=factory,
    )

    with pytest.raises(RuntimeError):

        await provider.execute(
            create_request(),
        )