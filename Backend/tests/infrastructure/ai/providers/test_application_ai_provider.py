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
from app.infrastructure.ai.exceptions.ai_client_exception import AIClientException
from app.infrastructure.ai.exceptions.ai_provider_exception import (
    AIProviderException,
)


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


@pytest.mark.asyncio
async def test_health_check_all_reports_every_configured_provider():
    gemini = AsyncMock()
    gemini.health_check.return_value = True
    openai = AsyncMock()
    openai.health_check.return_value = False

    provider = ApplicationAIProvider(
        providers={"gemini": gemini, "openai": openai}
    )

    assert await provider.health_check_all() == {
        "gemini": True,
        "openai": False,
    }


@pytest.mark.asyncio
async def test_execute_without_fallback_configured_raises_original_error():
    infra = AsyncMock()
    infra.execute.side_effect = AIProviderException("Gemini failed.")
    provider = ApplicationAIProvider(providers={"gemini": infra})

    with pytest.raises(AIProviderException, match="Gemini failed"):
        await provider.execute(create_request())


@pytest.mark.asyncio
async def test_execute_falls_back_to_next_configured_provider():
    gemini = AsyncMock()
    gemini.execute.side_effect = AIProviderException("model deprecated")

    fallback_response = create_response()
    openai = AsyncMock()
    openai.execute.return_value = fallback_response

    provider = ApplicationAIProvider(
        providers={"gemini": gemini, "openai": openai},
        fallback_order=["openai"],
        default_models={"openai": "gpt-4.1"},
    )

    result = await provider.execute(create_request())

    assert result is fallback_response
    gemini.execute.assert_awaited_once()
    openai.execute.assert_awaited_once()
    sent_request = openai.execute.await_args.args[0]
    assert sent_request.provider.value == "openai"
    assert sent_request.model.value == "gpt-4.1"


@pytest.mark.asyncio
async def test_execute_skips_fallback_provider_with_no_default_model():
    gemini = AsyncMock()
    gemini.execute.side_effect = AIClientException("no API key configured")

    azure = AsyncMock()
    azure.execute.return_value = create_response()

    provider = ApplicationAIProvider(
        providers={"gemini": gemini, "openai": azure},
        fallback_order=["openai"],
        default_models={},  # no default model known for "openai"
    )

    with pytest.raises(AIClientException):
        await provider.execute(create_request())

    azure.execute.assert_not_awaited()


@pytest.mark.asyncio
async def test_execute_raises_last_error_when_every_fallback_fails():
    gemini = AsyncMock()
    gemini.execute.side_effect = AIProviderException("gemini down")

    openai = AsyncMock()
    openai.execute.side_effect = AIProviderException("openai down too")

    provider = ApplicationAIProvider(
        providers={"gemini": gemini, "openai": openai},
        fallback_order=["openai"],
        default_models={"openai": "gpt-4.1"},
    )

    with pytest.raises(AIProviderException, match="openai down too"):
        await provider.execute(create_request())


@pytest.mark.asyncio
async def test_execute_does_not_retry_the_primary_provider_as_its_own_fallback():
    gemini = AsyncMock()
    gemini.execute.side_effect = AIProviderException("gemini down")

    provider = ApplicationAIProvider(
        providers={"gemini": gemini},
        fallback_order=["gemini"],
        default_models={"gemini": "gemini-3.5-flash"},
    )

    with pytest.raises(AIProviderException):
        await provider.execute(create_request())

    gemini.execute.assert_awaited_once()
