from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

import app.infrastructure.ai.clients.azure_openai_client as module
from app.infrastructure.ai.clients.azure_openai_client import AzureOpenAIClient
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


def _configured_settings(**overrides) -> ProviderSettings:
    defaults = dict(
        provider_name="azure_openai",
        api_key="secret",
        endpoint="https://example.openai.azure.com",
        api_version="2025-01-01-preview",
    )
    defaults.update(overrides)
    return ProviderSettings(**defaults)


def _install_fake_sdk(monkeypatch, response=None, side_effect=None):
    fake_client_instance = MagicMock()
    fake_client_instance.chat.completions.create = AsyncMock(return_value=response, side_effect=side_effect)
    fake_azure_cls = MagicMock(return_value=fake_client_instance)
    monkeypatch.setattr(module, "AsyncAzureOpenAI", fake_azure_cls)
    return fake_client_instance


@pytest.mark.asyncio
async def test_send_request_uses_deployment_name(monkeypatch):
    instance = _install_fake_sdk(monkeypatch, response=_fake_response())
    client = AzureOpenAIClient(_configured_settings())

    result = await client.send_request({"deployment": "my-gpt4-deployment", "contents": "hi", "temperature": 0.1, "max_tokens": 100})

    assert result == {"content": "Hello.", "finish_reason": "stop", "prompt_tokens": 10, "completion_tokens": 5}
    instance.chat.completions.create.assert_awaited_once()
    assert instance.chat.completions.create.await_args.kwargs["model"] == "my-gpt4-deployment"


@pytest.mark.asyncio
async def test_send_request_falls_back_to_model_key_when_no_deployment(monkeypatch):
    instance = _install_fake_sdk(monkeypatch, response=_fake_response())
    client = AzureOpenAIClient(_configured_settings())

    await client.send_request({"model": "my-gpt4-deployment", "contents": "hi"})

    assert instance.chat.completions.create.await_args.kwargs["model"] == "my-gpt4-deployment"


@pytest.mark.asyncio
async def test_send_request_raises_when_endpoint_missing(monkeypatch):
    _install_fake_sdk(monkeypatch, response=_fake_response())
    client = AzureOpenAIClient(_configured_settings(endpoint=None, enabled=False))

    with pytest.raises(AIClientException, match="must all be configured"):
        await client.send_request({"deployment": "d", "contents": "hi"})


@pytest.mark.asyncio
async def test_send_request_raises_when_sdk_not_installed(monkeypatch):
    monkeypatch.setattr(module, "AsyncAzureOpenAI", None)
    client = AzureOpenAIClient(_configured_settings())

    with pytest.raises(AIClientException, match="not installed"):
        await client.send_request({"deployment": "d", "contents": "hi"})


@pytest.mark.asyncio
async def test_send_request_wraps_sdk_exceptions(monkeypatch):
    _install_fake_sdk(monkeypatch, side_effect=RuntimeError("network error"))
    client = AzureOpenAIClient(_configured_settings())

    with pytest.raises(AIClientException):
        await client.send_request({"deployment": "d", "contents": "hi"})


@pytest.mark.asyncio
async def test_health_check_false_when_not_fully_configured(monkeypatch):
    _install_fake_sdk(monkeypatch, response=_fake_response())
    client = AzureOpenAIClient(_configured_settings(api_key=None, enabled=False))
    assert await client.health_check() is False
