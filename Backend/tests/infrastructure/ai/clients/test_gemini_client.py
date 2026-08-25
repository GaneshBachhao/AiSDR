from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

import app.infrastructure.ai.clients.gemini_client as module
from app.infrastructure.ai.clients.gemini_client import GeminiClient
from app.infrastructure.ai.configuration import ProviderSettings
from app.infrastructure.ai.exceptions.ai_client_exception import AIClientException
from app.infrastructure.ai.exceptions.ai_rate_limit_exception import AIRateLimitException
from app.infrastructure.configuration.gemini_settings import GeminiSettings

# Every test below passes an explicit GeminiSettings (usually with
# gemini_api_key_2="") rather than letting GeminiClient fall back to reading
# the real .env -- otherwise these tests would silently pick up whatever
# second key happens to be configured on a given machine, exactly the kind
# of non-hermetic failure a settings-reading class invites if a test forgets
# to override it (see TavilySettings tests for the same discipline).
_NO_SECOND_KEY = GeminiSettings(gemini_api_key_2="")


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


def _install_fake_sdk_per_key(monkeypatch, behavior_by_key: dict[str, dict]):
    """Like _install_fake_sdk, but genai.Client(api_key=...) returns a
    distinct fake instance per key, each with its own response/side_effect --
    needed to test fail-over between two real, different keys."""
    instances_by_key: dict[str, MagicMock] = {}
    for key, behavior in behavior_by_key.items():
        instance = MagicMock()
        instance.aio.models.generate_content = AsyncMock(
            return_value=behavior.get("response"), side_effect=behavior.get("side_effect")
        )
        instances_by_key[key] = instance

    fake_genai = MagicMock()
    fake_genai.Client.side_effect = lambda api_key: instances_by_key[api_key]
    monkeypatch.setattr(module, "genai", fake_genai)
    monkeypatch.setattr(module, "genai_types", MagicMock())
    return instances_by_key


def _rate_limit_error():
    from google.genai import errors as genai_errors

    return genai_errors.ClientError(
        429,
        {"error": {"code": 429, "status": "RESOURCE_EXHAUSTED", "message": "Quota exceeded"}},
    )


@pytest.mark.asyncio
async def test_send_request_returns_mapped_raw_response(monkeypatch):
    _install_fake_sdk(monkeypatch, response=_fake_response())
    client = GeminiClient(ProviderSettings(provider_name="gemini", api_key="secret"), _NO_SECOND_KEY)

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
    client = GeminiClient(
        ProviderSettings(provider_name="gemini", api_key=None, enabled=False), _NO_SECOND_KEY
    )

    with pytest.raises(AIClientException, match="no API key"):
        await client.send_request({"model": "gemini-2.5-pro", "contents": "hi"})


@pytest.mark.asyncio
async def test_send_request_raises_when_sdk_not_installed(monkeypatch):
    monkeypatch.setattr(module, "genai", None)
    client = GeminiClient(ProviderSettings(provider_name="gemini", api_key="secret"), _NO_SECOND_KEY)

    with pytest.raises(AIClientException, match="not installed"):
        await client.send_request({"model": "gemini-2.5-pro", "contents": "hi"})


@pytest.mark.asyncio
async def test_send_request_wraps_sdk_exceptions(monkeypatch):
    _install_fake_sdk(monkeypatch, side_effect=RuntimeError("network error"))
    client = GeminiClient(ProviderSettings(provider_name="gemini", api_key="secret"), _NO_SECOND_KEY)

    with pytest.raises(AIClientException):
        await client.send_request({"model": "gemini-2.5-pro", "contents": "hi"})


@pytest.mark.asyncio
async def test_send_request_raises_rate_limit_exception_on_429(monkeypatch):
    from google.genai import errors as genai_errors

    error = genai_errors.ClientError(
        429,
        {
            "error": {
                "code": 429,
                "status": "RESOURCE_EXHAUSTED",
                "message": "Quota exceeded",
                "details": [
                    {
                        "@type": "type.googleapis.com/google.rpc.RetryInfo",
                        "retryDelay": "14s",
                    }
                ],
            }
        },
    )
    _install_fake_sdk(monkeypatch, side_effect=error)
    client = GeminiClient(ProviderSettings(provider_name="gemini", api_key="secret"), _NO_SECOND_KEY)

    with pytest.raises(AIRateLimitException) as exc_info:
        await client.send_request({"model": "gemini-2.5-pro", "contents": "hi"})

    assert exc_info.value.retry_after_seconds == 14.0


@pytest.mark.asyncio
async def test_send_request_does_not_raise_rate_limit_for_a_non_429_client_error(monkeypatch):
    from google.genai import errors as genai_errors

    error = genai_errors.ClientError(400, {"error": {"code": 400, "status": "INVALID_ARGUMENT"}})
    _install_fake_sdk(monkeypatch, side_effect=error)
    client = GeminiClient(ProviderSettings(provider_name="gemini", api_key="secret"), _NO_SECOND_KEY)

    with pytest.raises(AIClientException) as exc_info:
        await client.send_request({"model": "gemini-2.5-pro", "contents": "hi"})

    assert not isinstance(exc_info.value, AIRateLimitException)


@pytest.mark.asyncio
async def test_health_check_true_when_configured(monkeypatch):
    _install_fake_sdk(monkeypatch, response=_fake_response())
    client = GeminiClient(ProviderSettings(provider_name="gemini", api_key="secret"), _NO_SECOND_KEY)
    assert await client.health_check() is True


@pytest.mark.asyncio
async def test_health_check_false_without_key(monkeypatch):
    _install_fake_sdk(monkeypatch, response=_fake_response())
    client = GeminiClient(
        ProviderSettings(provider_name="gemini", api_key=None, enabled=False), _NO_SECOND_KEY
    )
    assert await client.health_check() is False


# ---------------------------------------------------------------------------
# Dual-key fail-over (EPIC: Gemini key rotation)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_no_second_key_configured_behaves_exactly_like_single_key(monkeypatch):
    """Regression guard: leaving GEMINI_API_KEY_2 unset must not change
    behavior at all -- a 429 on key 1 propagates immediately, same as today."""
    _install_fake_sdk(monkeypatch, side_effect=_rate_limit_error())
    client = GeminiClient(ProviderSettings(provider_name="gemini", api_key="key-1"), _NO_SECOND_KEY)

    with pytest.raises(AIRateLimitException):
        await client.send_request({"model": "gemini-2.5-pro", "contents": "hi"})


@pytest.mark.asyncio
async def test_key_1_success_never_touches_key_2(monkeypatch):
    instances = _install_fake_sdk_per_key(
        monkeypatch,
        {"key-1": {"response": _fake_response(text="from key 1")}, "key-2": {"response": _fake_response()}},
    )
    client = GeminiClient(
        ProviderSettings(provider_name="gemini", api_key="key-1"),
        GeminiSettings(gemini_api_key_2="key-2"),
    )

    result = await client.send_request({"model": "gemini-2.5-pro", "contents": "hi"})

    assert result["content"] == "from key 1"
    instances["key-2"].aio.models.generate_content.assert_not_called()


@pytest.mark.asyncio
async def test_key_1_rate_limited_fails_over_to_key_2_automatically(monkeypatch):
    _install_fake_sdk_per_key(
        monkeypatch,
        {
            "key-1": {"side_effect": _rate_limit_error()},
            "key-2": {"response": _fake_response(text="from key 2")},
        },
    )
    client = GeminiClient(
        ProviderSettings(provider_name="gemini", api_key="key-1"),
        GeminiSettings(gemini_api_key_2="key-2"),
    )

    result = await client.send_request({"model": "gemini-2.5-pro", "contents": "hi"})

    assert result["content"] == "from key 2"


@pytest.mark.asyncio
async def test_next_call_starts_on_the_last_known_good_key(monkeypatch):
    """After failing over once, a later call shouldn't waste an attempt
    re-trying the already-exhausted key first."""
    instances = _install_fake_sdk_per_key(
        monkeypatch,
        {
            "key-1": {"side_effect": _rate_limit_error()},
            "key-2": {"response": _fake_response(text="from key 2")},
        },
    )
    client = GeminiClient(
        ProviderSettings(provider_name="gemini", api_key="key-1"),
        GeminiSettings(gemini_api_key_2="key-2"),
    )

    await client.send_request({"model": "gemini-2.5-pro", "contents": "hi"})
    instances["key-1"].aio.models.generate_content.reset_mock()
    instances["key-2"].aio.models.generate_content.reset_mock()

    await client.send_request({"model": "gemini-2.5-pro", "contents": "hi again"})

    instances["key-1"].aio.models.generate_content.assert_not_called()
    instances["key-2"].aio.models.generate_content.assert_called_once()


@pytest.mark.asyncio
async def test_both_keys_rate_limited_raises_rate_limit_exception(monkeypatch):
    _install_fake_sdk_per_key(
        monkeypatch,
        {"key-1": {"side_effect": _rate_limit_error()}, "key-2": {"side_effect": _rate_limit_error()}},
    )
    client = GeminiClient(
        ProviderSettings(provider_name="gemini", api_key="key-1"),
        GeminiSettings(gemini_api_key_2="key-2"),
    )

    with pytest.raises(AIRateLimitException):
        await client.send_request({"model": "gemini-2.5-pro", "contents": "hi"})


@pytest.mark.asyncio
async def test_health_check_true_with_only_second_key_configured(monkeypatch):
    _install_fake_sdk(monkeypatch, response=_fake_response())
    client = GeminiClient(
        ProviderSettings(provider_name="gemini", api_key=None, enabled=False),
        GeminiSettings(gemini_api_key_2="key-2"),
    )
    assert await client.health_check() is True
