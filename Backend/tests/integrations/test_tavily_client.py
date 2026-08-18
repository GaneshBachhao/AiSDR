from __future__ import annotations

from unittest.mock import Mock

import pytest
from tavily import UsageLimitExceededError

import app.integrations.tavily.tavily_client as module
from app.infrastructure.configuration.tavily_settings import TavilySettings
from app.integrations.tavily.exceptions import TavilyRateLimitException
from app.integrations.tavily.tavily_client import AgneticTavilyClient


def test_tavily_search_returns_results_from_sdk(monkeypatch) -> None:
    sdk = Mock()
    sdk.search.return_value = {"results": [{"title": "Example Manufacturing", "url": "https://example.com"}]}
    monkeypatch.setattr(module, "TavilyClient", Mock(return_value=sdk))

    client = AgneticTavilyClient(api_key="test-key")
    results = client.search("Manufacturing companies in Pune", max_results=5)

    assert results == [{"title": "Example Manufacturing", "url": "https://example.com"}]
    sdk.search.assert_called_once()


def test_tavily_search_is_safe_when_sdk_is_unavailable(monkeypatch) -> None:
    monkeypatch.setattr(module, "TavilyClient", None)
    client = AgneticTavilyClient(api_key="test-key")
    assert client.search("test") == []


def test_tavily_client_reads_key_from_settings_when_not_passed_explicitly(monkeypatch) -> None:
    sdk = Mock()
    sdk.search.return_value = {"results": []}
    monkeypatch.setattr(module, "TavilyClient", Mock(return_value=sdk))

    client = AgneticTavilyClient(settings=TavilySettings(tavily_api_key="from-settings"))
    client.search("test")

    module.TavilyClient.assert_called_once_with(api_key="from-settings")


def test_tavily_client_is_unconfigured_without_key_or_explicit_settings(monkeypatch) -> None:
    monkeypatch.setattr(module, "TavilyClient", Mock())
    client = AgneticTavilyClient(settings=TavilySettings(tavily_api_key=""))
    assert client.client is None
    assert client.search("test") == []


def test_tavily_search_raises_rate_limit_exception_on_usage_limit_exceeded(monkeypatch, caplog) -> None:
    sdk = Mock()
    sdk.search.side_effect = UsageLimitExceededError("Usage limit exceeded")
    monkeypatch.setattr(module, "TavilyClient", Mock(return_value=sdk))

    client = AgneticTavilyClient(api_key="test-key")
    with caplog.at_level("WARNING"):
        with pytest.raises(TavilyRateLimitException):
            client.search("Manufacturing companies in Pune")

    assert "RATE_LIMIT" in caplog.text


def test_tavily_search_swallows_other_errors_and_returns_empty_list(monkeypatch) -> None:
    sdk = Mock()
    sdk.search.side_effect = RuntimeError("network error")
    monkeypatch.setattr(module, "TavilyClient", Mock(return_value=sdk))

    client = AgneticTavilyClient(api_key="test-key")
    assert client.search("test") == []


def test_missing_sdk_and_missing_key_produce_distinct_warnings(monkeypatch, caplog) -> None:
    monkeypatch.setattr(module, "TavilyClient", None)
    client = AgneticTavilyClient(settings=TavilySettings(tavily_api_key=""))
    with caplog.at_level("WARNING"):
        client.search("test")
    assert "tavily-python" in caplog.text
    assert "not installed" in caplog.text
