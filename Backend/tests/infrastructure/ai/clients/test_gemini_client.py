from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

import app.infrastructure.ai.clients.gemini_client as module
from app.infrastructure.ai.clients.gemini_client import GeminiClient
from app.infrastructure.ai.configuration import ProviderSettings
from app.infrastructure.ai.exceptions.ai_client_exception import AIClientException


def _fake_response(text="Hello.", finish_reason_name="STOP", prompt_tokens=10, completion_tokens=5):
    finish_reason = MagicMock()
    finish_reason.name = finish_reason_name
    candidate = MagicMock()
    candidate.finish_reason = finish_reason
    from google.genai import types as genai_types

    usage = MagicMock(spec=genai_types.GenerateContentResponseUsageMetadata)
    usage.prompt_token_count = prompt_tokens
    usage.candidates_token_count = completion_tokens
    response = MagicMock()
    response.text = text
    response.candidates = [candidate]
    response.usage_metadata = usage
    return response


def _install_fake_sdk(monkeypatch, response=None, side_effect=None):
    fake_client_instance = MagicMock()
    fake_client_instance.aio.models.generate_content = AsyncMock(
        return_value=response, side_effect=side_effect
    )
    fake_genai = MagicMock()
    fake_genai.Client.return_value = fake_client_instance
    monkeypatch.setattr(module, "genai", fake_genai)
    monkeypatch.setattr(module, "genai_types", MagicMock())
    return fake_client_instance


@pytest.mark.asyncio
async def test_send_request_returns_mapped_raw_response(monkeypatch):
    _install_fake_sdk(monkeypatch, response=_fake_response())
    client = GeminiClient(ProviderSettings(provider_name="gemini", api_key="secret"))

    result = await client.send_request(
        {"model": "gemini-2.5-pro", "contents": "hi", "temperature": 0.1, "max_tokens": 100}
    )

    assert result == {
        "content": "Hello.",
        "finish_reason": "STOP",
        "prompt_tokens": 10,
        "completion_tokens": 5,
    }


@pytest.mark.asyncio
async def test_send_request_raises_when_no_api_key(monkeypatch):
    _install_fake_sdk(monkeypatch, response=_fake_response())
    client = GeminiClient(ProviderSettings(provider_name="gemini", api_key=None, enabled=False))

    with pytest.raises(AIClientException, match="no API key"):
        await client.send_request({"model": "gemini-2.5-pro", "contents": "hi"})


@pytest.mark.asyncio
async def test_send_request_raises_when_sdk_not_installed(monkeypatch):
    monkeypatch.setattr(module, "genai", None)
    client = GeminiClient(ProviderSettings(provider_name="gemini", api_key="secret"))

    with pytest.raises(AIClientException, match="not installed"):
        await client.send_request({"model": "gemini-2.5-pro", "contents": "hi"})


@pytest.mark.asyncio
async def test_send_request_wraps_sdk_exceptions(monkeypatch):
    _install_fake_sdk(monkeypatch, side_effect=RuntimeError("network error"))
    client = GeminiClient(ProviderSettings(provider_name="gemini", api_key="secret"))

    with pytest.raises(AIClientException):
        await client.send_request({"model": "gemini-2.5-pro", "contents": "hi"})


@pytest.mark.asyncio
async def test_health_check_true_when_configured(monkeypatch):
    _install_fake_sdk(monkeypatch, response=_fake_response())
    client = GeminiClient(ProviderSettings(provider_name="gemini", api_key="secret"))
    assert await client.health_check() is True


@pytest.mark.asyncio
async def test_health_check_false_without_key(monkeypatch):
    _install_fake_sdk(monkeypatch, response=_fake_response())
    client = GeminiClient(ProviderSettings(provider_name="gemini", api_key=None, enabled=False))
    assert await client.health_check() is False
