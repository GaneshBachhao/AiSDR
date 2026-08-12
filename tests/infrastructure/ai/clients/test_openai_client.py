from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

import app.infrastructure.ai.clients.openai_client as module
from app.infrastructure.ai.clients.openai_client import OpenAIClient
from app.infrastructure.ai.configuration import ProviderSettings
from app.infrastructure.ai.exceptions.ai_client_exception import AIClientException


def _fake_response(content="Hello.", finish_reason="stop", prompt_tokens=10, completion_tokens=5):
    message = MagicMock()
    message.content = content
    choice = MagicMock()
    choice.message = message
    choice.finish_reason = finish_reason
    usage = MagicMock()
    usage.prompt_tokens = prompt_tokens
    usage.completion_tokens = completion_tokens
    response = MagicMock()
    response.choices = [choice]
    response.usage = usage
    return response


def _install_fake_sdk(monkeypatch, response=None, side_effect=None):
    fake_client_instance = MagicMock()
    fake_client_instance.chat.completions.create = AsyncMock(return_value=response, side_effect=side_effect)
    fake_openai_cls = MagicMock(return_value=fake_client_instance)
    monkeypatch.setattr(module, "AsyncOpenAI", fake_openai_cls)
    return fake_client_instance


@pytest.mark.asyncio
async def test_send_request_returns_mapped_raw_response(monkeypatch):
    _install_fake_sdk(monkeypatch, response=_fake_response())
    client = OpenAIClient(ProviderSettings(provider_name="openai", api_key="secret"))

    result = await client.send_request({"model": "gpt-4.1", "contents": "hi", "temperature": 0.1, "max_tokens": 100})

    assert result == {
        "content": "Hello.",
        "finish_reason": "stop",
        "prompt_tokens": 10,
        "completion_tokens": 5,
    }


@pytest.mark.asyncio
async def test_send_request_raises_when_no_api_key(monkeypatch):
    _install_fake_sdk(monkeypatch, response=_fake_response())
    client = OpenAIClient(ProviderSettings(provider_name="openai", api_key=None, enabled=False))

    with pytest.raises(AIClientException, match="no API key"):
        await client.send_request({"model": "gpt-4.1", "contents": "hi"})


@pytest.mark.asyncio
async def test_send_request_raises_when_sdk_not_installed(monkeypatch):
    monkeypatch.setattr(module, "AsyncOpenAI", None)
    client = OpenAIClient(ProviderSettings(provider_name="openai", api_key="secret"))

    with pytest.raises(AIClientException, match="not installed"):
        await client.send_request({"model": "gpt-4.1", "contents": "hi"})


@pytest.mark.asyncio
async def test_send_request_wraps_sdk_exceptions(monkeypatch):
    _install_fake_sdk(monkeypatch, side_effect=RuntimeError("network error"))
    client = OpenAIClient(ProviderSettings(provider_name="openai", api_key="secret"))

    with pytest.raises(AIClientException):
        await client.send_request({"model": "gpt-4.1", "contents": "hi"})


@pytest.mark.asyncio
async def test_health_check_true_when_configured(monkeypatch):
    _install_fake_sdk(monkeypatch, response=_fake_response())
    client = OpenAIClient(ProviderSettings(provider_name="openai", api_key="secret"))
    assert await client.health_check() is True


@pytest.mark.asyncio
async def test_health_check_false_without_key(monkeypatch):
    _install_fake_sdk(monkeypatch, response=_fake_response())
    client = OpenAIClient(ProviderSettings(provider_name="openai", api_key=None, enabled=False))
    assert await client.health_check() is False
