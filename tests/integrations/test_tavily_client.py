from __future__ import annotations

from unittest.mock import Mock

import app.integrations.tavily.tavily_client as module
from app.integrations.tavily.tavily_client import AgneticTavilyClient


def test_tavily_search_returns_results_from_sdk(monkeypatch) -> None:
    sdk = Mock()
    sdk.search.return_value = {
        "results": [
            {"title": "Example Manufacturing", "url": "https://example.com"}
        ]
    }
    monkeypatch.setattr(module, "TavilyClient", Mock(return_value=sdk))

    client = AgneticTavilyClient(api_key="test-key")
    results = client.search("Manufacturing companies in Pune", max_results=5)

    assert results == [
        {"title": "Example Manufacturing", "url": "https://example.com"}
    ]
    sdk.search.assert_called_once()


def test_tavily_search_is_safe_when_sdk_is_unavailable(monkeypatch) -> None:
    monkeypatch.setattr(module, "TavilyClient", None)
    client = AgneticTavilyClient(api_key="test-key")
    assert client.search("test") == []
