from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

import app.infrastructure.ai.clients.openrouter_client as module
from app.infrastructure.ai.clients.openrouter_client import OpenRouterClient
from app.infrastructure.ai.configuration import ProviderSettings
from app.infrastructure.ai.exceptions.ai_client_exception import AIClientException
from app.infrastructure.ai.exceptions.ai_rate_limit_exception import AIRateLimitException


def _settings(**overrides) -> ProviderSettings:
    defaults = {
        "provider_name": "openrouter",
        "api_key": "secret",
        "endpoint": "https://openrouter.ai/api/v1",
    }
    defaults.update(overrides)
    return ProviderSettings(**defaults)


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
    fake_async_openai = MagicMock(return_value=fake_client_instance)
    monkeypatch.setattr(module, "AsyncOpenAI", fake_async_openai)
    return fake_client_instance, fake_async_openai


def _rate_limit_error(retry_after="30"):
    from openai import RateLimitError

    req = httpx.Request("POST", "https://openrouter.ai/api/v1/chat/completions")
    headers = {"retry-after": retry_after} if retry_after else {}
    resp = httpx.Response(429, headers=headers, request=req)
    return RateLimitError("rate limited", response=resp, body=None)


@pytest.mark.asyncio
async def test_send_request_returns_mapped_raw_response(monkeypatch):
    _install_fake_sdk(monkeypatch, response=_fake_response())
    client = OpenRouterClient(_settings())

    result = await client.send_request({"model": "meta-llama/llama-3.3-70b-instruct:free", "contents": "hi"})

    assert result == {
        "content": "Hello.",
        "finish_reason": "stop",
        "prompt_tokens": 10,
        "completion_tokens": 5,
    }


def test_client_is_constructed_with_the_configured_base_url(monkeypatch):
    _, fake_async_openai = _install_fake_sdk(monkeypatch, response=_fake_response())

    OpenRouterClient(_settings(endpoint="https://openrouter.ai/api/v1"))

    fake_async_openai.assert_called_once_with(api_key="secret", base_url="https://openrouter.ai/api/v1")


@pytest.mark.asyncio
async def test_send_request_raises_when_no_api_key(monkeypatch):
    _install_fake_sdk(monkeypatch, response=_fake_response())
    client = OpenRouterClient(_settings(api_key=None, enabled=False))

    with pytest.raises(AIClientException, match="no API key"):
        await client.send_request({"model": "x", "contents": "hi"})


@pytest.mark.asyncio
async def test_send_request_raises_when_sdk_not_installed(monkeypatch):
    monkeypatch.setattr(module, "AsyncOpenAI", None)
    client = OpenRouterClient(_settings())

    with pytest.raises(AIClientException, match="not installed"):
        await client.send_request({"model": "x", "contents": "hi"})


@pytest.mark.asyncio
async def test_send_request_wraps_generic_sdk_exceptions(monkeypatch):
    _install_fake_sdk(monkeypatch, side_effect=RuntimeError("network error"))
    client = OpenRouterClient(_settings())

    with pytest.raises(AIClientException):
        await client.send_request({"model": "x", "contents": "hi"})


@pytest.mark.asyncio
async def test_send_request_raises_rate_limit_exception_on_429(monkeypatch):
    _install_fake_sdk(monkeypatch, side_effect=_rate_limit_error(retry_after="30"))
    client = OpenRouterClient(_settings())

    with pytest.raises(AIRateLimitException) as exc_info:
        await client.send_request({"model": "x", "contents": "hi"})

    assert exc_info.value.retry_after_seconds == 30.0


@pytest.mark.asyncio
async def test_send_request_rate_limit_without_retry_after_header_still_raises(monkeypatch):
    _install_fake_sdk(monkeypatch, side_effect=_rate_limit_error(retry_after=None))
    client = OpenRouterClient(_settings())

    with pytest.raises(AIRateLimitException) as exc_info:
        await client.send_request({"model": "x", "contents": "hi"})

    assert exc_info.value.retry_after_seconds is None


@pytest.mark.asyncio
async def test_health_check_true_when_configured(monkeypatch):
    _install_fake_sdk(monkeypatch, response=_fake_response())
    client = OpenRouterClient(_settings())
    assert await client.health_check() is True


@pytest.mark.asyncio
async def test_health_check_false_without_key(monkeypatch):
    _install_fake_sdk(monkeypatch, response=_fake_response())
    client = OpenRouterClient(_settings(api_key=None, enabled=False))
    assert await client.health_check() is False
