from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from app.domain.ai.aggregates.ai_request import AIRequest
from app.domain.ai.enums.finish_reason import FinishReason
from app.domain.ai.value_objects.max_tokens import MaxTokens
from app.domain.ai.value_objects.model_name import ModelName
from app.domain.ai.value_objects.prompt import Prompt
from app.domain.ai.value_objects.provider_name import ProviderName
from app.domain.ai.value_objects.temperature import Temperature
from app.infrastructure.ai.configuration import ProviderSettings
from app.infrastructure.ai.exceptions.ai_provider_exception import AIProviderException
from app.infrastructure.ai.providers.openai_provider import OpenAIProvider


def _request() -> AIRequest:
    return AIRequest(
        provider=ProviderName("openai"),
        model=ModelName("gpt-4.1"),
        prompt=Prompt("Explain Clean Architecture."),
        temperature=Temperature(0.2),
        max_tokens=MaxTokens(256),
    )


@pytest.mark.asyncio
async def test_execute_builds_ai_response_from_raw_dict():
    client = AsyncMock()
    client.send_request.return_value = {
        "content": "Clean Architecture separates concerns into layers.",
        "finish_reason": "stop",
        "prompt_tokens": 12,
        "completion_tokens": 20,
    }
    provider = OpenAIProvider(client, ProviderSettings(provider_name="openai", api_key="secret"))

    response = await provider.execute(_request())

    assert response.content == "Clean Architecture separates concerns into layers."
    assert response.finish_reason == FinishReason.STOP
    assert response.token_usage.prompt_tokens == 12
    assert response.token_usage.completion_tokens == 20


@pytest.mark.asyncio
async def test_execute_sends_prompt_text_not_message_objects():
    client = AsyncMock()
    client.send_request.return_value = {"content": "ok", "finish_reason": "stop", "prompt_tokens": 1, "completion_tokens": 1}
    provider = OpenAIProvider(client, ProviderSettings(provider_name="openai", api_key="secret"))

    request = _request()
    await provider.execute(request)

    sent_payload = client.send_request.await_args.args[0]
    assert sent_payload["contents"] == request.prompt.value
    assert sent_payload["model"] == "gpt-4.1"


@pytest.mark.asyncio
async def test_execute_maps_tool_calls_finish_reason_to_tool_call():
    client = AsyncMock()
    client.send_request.return_value = {"content": "...", "finish_reason": "tool_calls", "prompt_tokens": 1, "completion_tokens": 1}
    provider = OpenAIProvider(client, ProviderSettings(provider_name="openai", api_key="secret"))

    response = await provider.execute(_request())
    assert response.finish_reason == FinishReason.TOOL_CALL


@pytest.mark.asyncio
async def test_execute_wraps_client_exceptions():
    client = AsyncMock()
    client.send_request.side_effect = RuntimeError("boom")
    provider = OpenAIProvider(client, ProviderSettings(provider_name="openai", api_key="secret"))

    with pytest.raises(AIProviderException):
        await provider.execute(_request())


@pytest.mark.asyncio
async def test_health_check_delegates_to_client():
    client = AsyncMock()
    client.health_check.return_value = True
    provider = OpenAIProvider(client, ProviderSettings(provider_name="openai", api_key="secret"))
    assert await provider.health_check() is True
