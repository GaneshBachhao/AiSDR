from __future__ import annotations

from unittest.mock import Mock

import pytest
from tavily import UsageLimitExceededError

import app.integrations.tavily.tavily_client as module
from app.infrastructure.configuration.tavily_settings import TavilySettings
from app.integrations.tavily.exceptions import TavilyRateLimitException
from app.integrations.tavily.tavily_client import AgneticTavilyClient

# Every test below passes an explicit TavilySettings (usually with
# tavily_api_key_2="") rather than letting AgneticTavilyClient fall back to
# reading the real .env -- otherwise these tests would silently pick up
# whatever second key happens to be configured on a given machine, exactly
# the kind of non-hermetic failure a settings-reading class invites if a
# test forgets to override it (same discipline as test_gemini_client.py).
_NO_SECOND_KEY = TavilySettings(tavily_api_key_2="")


def test_tavily_search_returns_results_from_sdk(monkeypatch) -> None:
    sdk = Mock()
    sdk.search.return_value = {"results": [{"title": "Example Manufacturing", "url": "https://example.com"}]}
    monkeypatch.setattr(module, "TavilyClient", Mock(return_value=sdk))

    client = AgneticTavilyClient(api_key="test-key", settings=_NO_SECOND_KEY)
    results = client.search("Manufacturing companies in Pune", max_results=5)

    assert results == [{"title": "Example Manufacturing", "url": "https://example.com"}]
    sdk.search.assert_called_once()


def test_tavily_search_is_safe_when_sdk_is_unavailable(monkeypatch) -> None:
    monkeypatch.setattr(module, "TavilyClient", None)
    client = AgneticTavilyClient(api_key="test-key", settings=_NO_SECOND_KEY)
    assert client.search("test") == []


def test_tavily_client_reads_key_from_settings_when_not_passed_explicitly(monkeypatch) -> None:
    sdk = Mock()
    sdk.search.return_value = {"results": []}
    monkeypatch.setattr(module, "TavilyClient", Mock(return_value=sdk))

    client = AgneticTavilyClient(settings=TavilySettings(tavily_api_key="from-settings", tavily_api_key_2=""))
    client.search("test")

    module.TavilyClient.assert_called_once_with(api_key="from-settings")


def test_tavily_client_is_unconfigured_without_key_or_explicit_settings(monkeypatch) -> None:
    monkeypatch.setattr(module, "TavilyClient", Mock())
    client = AgneticTavilyClient(settings=TavilySettings(tavily_api_key="", tavily_api_key_2=""))
    assert client.client is None
    assert client.search("test") == []


def test_tavily_search_raises_rate_limit_exception_on_usage_limit_exceeded(monkeypatch, caplog) -> None:
    sdk = Mock()
    sdk.search.side_effect = UsageLimitExceededError("Usage limit exceeded")
    monkeypatch.setattr(module, "TavilyClient", Mock(return_value=sdk))

    client = AgneticTavilyClient(api_key="test-key", settings=_NO_SECOND_KEY)
    with caplog.at_level("WARNING"):
        with pytest.raises(TavilyRateLimitException):
            client.search("Manufacturing companies in Pune")

    assert "RATE_LIMIT" in caplog.text


def test_tavily_search_swallows_other_errors_and_returns_empty_list(monkeypatch) -> None:
    sdk = Mock()
    sdk.search.side_effect = RuntimeError("network error")
    monkeypatch.setattr(module, "TavilyClient", Mock(return_value=sdk))

    client = AgneticTavilyClient(api_key="test-key", settings=_NO_SECOND_KEY)
    assert client.search("test") == []


def test_missing_sdk_and_missing_key_produce_distinct_warnings(monkeypatch, caplog) -> None:
    monkeypatch.setattr(module, "TavilyClient", None)
    client = AgneticTavilyClient(settings=TavilySettings(tavily_api_key="", tavily_api_key_2=""))
    with caplog.at_level("WARNING"):
        client.search("test")
    assert "tavily-python" in caplog.text
    assert "not installed" in caplog.text


# ---------------------------------------------------------------------------
# Dual-key fail-over
# ---------------------------------------------------------------------------


def _install_fake_sdk_per_key(monkeypatch, behavior_by_key: dict[str, dict]):
    """Like the single-instance mock above, but TavilyClient(api_key=...)
    returns a distinct fake instance per key, each with its own
    return_value/side_effect -- needed to test fail-over between two real,
    different keys."""
    instances_by_key: dict[str, Mock] = {}
    for key, behavior in behavior_by_key.items():
        instance = Mock()
        if "side_effect" in behavior:
            instance.search.side_effect = behavior["side_effect"]
        else:
            instance.search.return_value = behavior.get("response", {"results": []})
        instances_by_key[key] = instance

    fake_tavily_client = Mock(side_effect=lambda api_key: instances_by_key[api_key])
    monkeypatch.setattr(module, "TavilyClient", fake_tavily_client)
    return instances_by_key


def test_no_second_key_configured_behaves_exactly_like_single_key(monkeypatch) -> None:
    """Regression guard: leaving TAVILY_API_KEY_2 unset must not change
    behavior at all -- a usage-limit error on key 1 propagates immediately,
    same as today."""
    sdk = Mock()
    sdk.search.side_effect = UsageLimitExceededError("Usage limit exceeded")
    monkeypatch.setattr(module, "TavilyClient", Mock(return_value=sdk))

    client = AgneticTavilyClient(api_key="key-1", settings=_NO_SECOND_KEY)

    with pytest.raises(TavilyRateLimitException):
        client.search("test")


def test_key_1_success_never_touches_key_2(monkeypatch) -> None:
    instances = _install_fake_sdk_per_key(
        monkeypatch,
        {
            "key-1": {"response": {"results": [{"title": "from key 1"}]}},
            "key-2": {"response": {"results": []}},
        },
    )
    client = AgneticTavilyClient(settings=TavilySettings(tavily_api_key="key-1", tavily_api_key_2="key-2"))

    results = client.search("test")

    assert results == [{"title": "from key 1"}]
    instances["key-2"].search.assert_not_called()


def test_key_1_rate_limited_fails_over_to_key_2_automatically(monkeypatch) -> None:
    _install_fake_sdk_per_key(
        monkeypatch,
        {
            "key-1": {"side_effect": UsageLimitExceededError("exhausted")},
            "key-2": {"response": {"results": [{"title": "from key 2"}]}},
        },
    )
    client = AgneticTavilyClient(settings=TavilySettings(tavily_api_key="key-1", tavily_api_key_2="key-2"))

    results = client.search("test")

    assert results == [{"title": "from key 2"}]


def test_next_call_starts_on_the_last_known_good_key(monkeypatch) -> None:
    """After failing over once, a later call shouldn't waste an attempt
    re-trying the already-exhausted key first."""
    instances = _install_fake_sdk_per_key(
        monkeypatch,
        {
            "key-1": {"side_effect": UsageLimitExceededError("exhausted")},
            "key-2": {"response": {"results": [{"title": "from key 2"}]}},
        },
    )
    client = AgneticTavilyClient(settings=TavilySettings(tavily_api_key="key-1", tavily_api_key_2="key-2"))

    client.search("first call")
    instances["key-1"].search.reset_mock()
    instances["key-2"].search.reset_mock()

    client.search("second call")

    instances["key-1"].search.assert_not_called()
    instances["key-2"].search.assert_called_once()


def test_both_keys_rate_limited_raises_rate_limit_exception(monkeypatch) -> None:
    _install_fake_sdk_per_key(
        monkeypatch,
        {
            "key-1": {"side_effect": UsageLimitExceededError("exhausted")},
            "key-2": {"side_effect": UsageLimitExceededError("also exhausted")},
        },
    )
    client = AgneticTavilyClient(settings=TavilySettings(tavily_api_key="key-1", tavily_api_key_2="key-2"))

    with pytest.raises(TavilyRateLimitException):
        client.search("test")
