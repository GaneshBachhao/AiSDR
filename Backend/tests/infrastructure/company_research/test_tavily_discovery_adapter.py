from __future__ import annotations

from unittest.mock import Mock

import pytest

from app.application.company_research.dto.company_research_request import (
    CompanyResearchRequest,
)
from app.infrastructure.company_research.tavily_discovery_adapter import (
    TavilyDiscoveryAdapter,
)
from app.infrastructure.configuration.company_research_settings import (
    CompanyResearchSettings,
)
from app.integrations.tavily.exceptions import TavilyRateLimitException


def _client_returning(results: list[dict]) -> Mock:
    client = Mock()
    client.search.return_value = results
    return client


@pytest.mark.asyncio
async def test_discover_returns_candidate_for_a_plain_company_result():
    client = _client_returning(
        [
            {
                "title": "Acme Manufacturing | Official Site",
                "url": "https://acme.example/about",
                "content": "Acme Manufacturing produces industrial equipment.",
            }
        ]
    )
    adapter = TavilyDiscoveryAdapter(client=client, settings=CompanyResearchSettings())
    request = CompanyResearchRequest(geography="India", industries=["Manufacturing"], number_of_companies=2)

    candidates = await adapter.discover(request)

    assert len(candidates) == 1
    assert candidates[0].company_name == "Acme Manufacturing"
    assert candidates[0].website == "https://acme.example"


@pytest.mark.asyncio
async def test_discover_returns_empty_pool_when_every_query_is_rate_limited(caplog):
    """Matches what a real fully-rate-limited discovery pass looks like:
    an empty candidate pool, same as "genuinely no results," but now
    clearly logged (RATE_LIMIT) so it's distinguishable in practice, and
    no exception crashes the whole search."""
    client = Mock()
    client.search.side_effect = TavilyRateLimitException("Tavily usage limit exceeded")
    adapter = TavilyDiscoveryAdapter(client=client, settings=CompanyResearchSettings())
    request = CompanyResearchRequest(geography="India", industries=["Manufacturing"], number_of_companies=2)

    with caplog.at_level("WARNING"):
        candidates = await adapter.discover(request)

    assert candidates == []
    assert "RATE_LIMIT" in caplog.text


@pytest.mark.asyncio
async def test_discover_skips_blocked_domains():
    client = _client_returning(
        [{"title": "Acme on LinkedIn", "url": "https://linkedin.com/company/acme", "content": "x"}]
    )
    adapter = TavilyDiscoveryAdapter(client=client, settings=CompanyResearchSettings())
    request = CompanyResearchRequest(geography="India")

    candidates = await adapter.discover(request)
    assert candidates == []


@pytest.mark.asyncio
async def test_discover_skips_listicle_style_titles():
    client = _client_returning(
        [
            {
                "title": "Top 10 Manufacturing Companies in India",
                "url": "https://example.com/blog",
                "content": "x",
            }
        ]
    )
    adapter = TavilyDiscoveryAdapter(client=client, settings=CompanyResearchSettings())
    request = CompanyResearchRequest(geography="India")

    candidates = await adapter.discover(request)
    assert candidates == []


@pytest.mark.asyncio
async def test_discover_extracts_directory_rows_as_candidates_not_the_directory_itself():
    directory_content = (
        "Acme Manufacturing\nCountry\nIndia\nSales Revenue ($M)\n"
        "Beta Industries\nCountry\nIndia\nSales Revenue ($M)\n"
    )
    client = _client_returning(
        [
            {
                "title": "Manufacturing Company Directory - 500 records",
                "url": "https://directory.example/list",
                "content": directory_content,
            }
        ]
    )
    adapter = TavilyDiscoveryAdapter(client=client, settings=CompanyResearchSettings())
    request = CompanyResearchRequest(geography="India")

    candidates = await adapter.discover(request)

    names = {c.company_name for c in candidates}
    assert names == {"Acme Manufacturing", "Beta Industries"}
    for candidate in candidates:
        assert candidate.discovery_metadata
        assert candidate.discovery_metadata[0]["source_type"] == "discovery_directory"


@pytest.mark.asyncio
async def test_discover_deduplicates_by_normalized_name():
    client = _client_returning(
        [
            {"title": "Acme Manufacturing | Home", "url": "https://acme.example/", "content": "x"},
            {"title": "ACME MANUFACTURING - About", "url": "https://acme-mirror.example/", "content": "x"},
        ]
    )
    adapter = TavilyDiscoveryAdapter(client=client, settings=CompanyResearchSettings())
    request = CompanyResearchRequest(geography="India")

    candidates = await adapter.discover(request)
    assert len(candidates) == 1
