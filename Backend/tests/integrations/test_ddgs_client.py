from __future__ import annotations

from unittest.mock import Mock

import pytest

import app.integrations.ddgs.ddgs_client as module
from app.integrations.ddgs.ddgs_client import DdgsClient
from app.integrations.tavily.exceptions import TavilyRateLimitException


def test_ddgs_search_returns_tavily_shaped_results_from_sdk(monkeypatch) -> None:
    sdk = Mock()
    sdk.text.return_value = [
        {"title": "Example Manufacturing", "href": "https://example.com", "body": "snippet"}
    ]
    monkeypatch.setattr(module, "DDGS", Mock(return_value=sdk))

    client = DdgsClient()
    results = client.search("Manufacturing companies in Pune", max_results=5)

    assert results == [{"title": "Example Manufacturing", "url": "https://example.com", "content": "snippet"}]
    sent_query = sdk.text.call_args.args[0]
    assert sent_query.startswith("Manufacturing companies in Pune")
    assert sdk.text.call_args.kwargs == {"max_results": 5}


def test_ddgs_search_appends_noise_exclusion_terms_to_the_query(monkeypatch) -> None:
    sdk = Mock()
    sdk.text.return_value = []
    monkeypatch.setattr(module, "DDGS", Mock(return_value=sdk))

    DdgsClient().search("Manufacturing companies in Pune")

    sent_query = sdk.text.call_args.args[0]
    assert "-jobs" in sent_query
    assert "-directory" in sent_query


@pytest.mark.parametrize(
    ("title", "url"),
    [
        ("American Companies Directory -- Search 8,000+ US Companies", "https://americancompanies.com"),
        ("Manufacturing Hiring Trends 2026: Skills, Jobs, Key Challenges", "https://taggd.in"),
        ("National Manufacturers Database & Directories", "https://www.mni.net"),
        ("Made in America", "https://www.madeinamerica.gov"),
        ("Manufacturing.gov", "https://www.manufacturing.gov"),
        ("Used PVC Manufacturing Plants", "https://www.bing.com/search?q=x"),
    ],
)
def test_ddgs_search_filters_out_known_noise_categories(monkeypatch, title, url) -> None:
    sdk = Mock()
    sdk.text.return_value = [{"title": title, "href": url, "body": ""}]
    monkeypatch.setattr(module, "DDGS", Mock(return_value=sdk))

    results = DdgsClient().search("Manufacturing companies in India")

    assert results == []


@pytest.mark.parametrize(
    ("title", "url"),
    [
        # Real false positives observed live (EPIC: ddgs discovery tuning) --
        # a staffing consultancy whose own domain spells out its business
        # even though the raw title didn't contain any narrower phrase, and
        # a major newspaper portal caught by the known-news-domain list.
        ("Top Recruitment & Staffing Solutions in India | Shriniwas", "https://www.shriniwasplacements.com/"),
        ("Latest News, Breaking News, India News", "https://timesofindia.indiatimes.com/"),
    ],
)
def test_ddgs_search_filters_out_real_observed_false_positives(monkeypatch, title, url) -> None:
    sdk = Mock()
    sdk.text.return_value = [{"title": title, "href": url, "body": ""}]
    monkeypatch.setattr(module, "DDGS", Mock(return_value=sdk))

    results = DdgsClient().search("Manufacturing companies in India")

    assert results == []


def test_ddgs_search_keeps_a_genuine_company_result(monkeypatch) -> None:
    sdk = Mock()
    sdk.text.return_value = [
        {"title": "The Mahindra Group Official Website", "href": "https://www.mahindra.com", "body": "x"}
    ]
    monkeypatch.setattr(module, "DDGS", Mock(return_value=sdk))

    results = DdgsClient().search("Manufacturing companies in India")

    assert len(results) == 1
    assert results[0]["title"] == "The Mahindra Group Official Website"


def test_ddgs_search_is_safe_when_sdk_is_unavailable(monkeypatch) -> None:
    monkeypatch.setattr(module, "DDGS", None)
    client = DdgsClient()
    assert client.search("test") == []


def test_ddgs_search_raises_rate_limit_exception_on_ratelimit(monkeypatch, caplog) -> None:
    class FakeRatelimitException(Exception):
        pass

    sdk = Mock()
    sdk.text.side_effect = FakeRatelimitException("rate limited")
    monkeypatch.setattr(module, "DDGS", Mock(return_value=sdk))
    monkeypatch.setattr(module, "RatelimitException", FakeRatelimitException)

    client = DdgsClient()
    with caplog.at_level("WARNING"):
        with pytest.raises(TavilyRateLimitException):
            client.search("Manufacturing companies in Pune")

    assert "RATE_LIMIT" in caplog.text


def test_ddgs_search_swallows_other_errors_and_returns_empty_list(monkeypatch) -> None:
    sdk = Mock()
    sdk.text.side_effect = RuntimeError("network error")
    monkeypatch.setattr(module, "DDGS", Mock(return_value=sdk))

    client = DdgsClient()
    assert client.search("test") == []


def test_missing_sdk_produces_a_clear_warning(monkeypatch, caplog) -> None:
    monkeypatch.setattr(module, "DDGS", None)
    client = DdgsClient()
    with caplog.at_level("WARNING"):
        client.search("test")
    assert "ddgs" in caplog.text
    assert "not installed" in caplog.text
