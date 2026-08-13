from __future__ import annotations

from unittest.mock import Mock

import pytest

from app.application.company_research.dto.company_research_request import (
    CompanyResearchRequest,
)
from app.infrastructure.company_research.tavily_directory_adapter import (
    TavilyDirectoryAdapter,
)
from app.infrastructure.configuration.company_research_settings import (
    CompanyResearchSettings,
)


def _client_returning(results: list[dict]) -> Mock:
    client = Mock()
    client.search.return_value = results
    return client


_DIRECTORY_CONTENT = (
    "Acme Manufacturing\nCountry\nIndia\nSales Revenue ($M)\n"
    "Beta Industries\nCountry\nIndia\nSales Revenue ($M)\n"
)

_DIRECTORY_RESULT = {
    "title": "Manufacturing Company Directory - 500 records",
    "url": "https://directory.example/list",
    "content": _DIRECTORY_CONTENT,
}


@pytest.mark.asyncio
async def test_discover_extracts_directory_rows():
    client = _client_returning([_DIRECTORY_RESULT])
    adapter = TavilyDirectoryAdapter(client=client, settings=CompanyResearchSettings())
    request = CompanyResearchRequest(geography="India", industries=["Manufacturing"])

    candidates = await adapter.discover(request)

    names = {c.company_name for c in candidates}
    assert names == {"Acme Manufacturing", "Beta Industries"}
    for candidate in candidates:
        assert candidate.discovery_metadata
        assert candidate.discovery_metadata[0]["source_type"] == "discovery_directory"


@pytest.mark.asyncio
async def test_discover_skips_plain_single_company_results():
    """The defining difference from the expensive tier: a normal search
    result (not a directory page) yields no candidate at all here."""
    client = _client_returning(
        [
            {
                "title": "Acme Manufacturing | Official Site",
                "url": "https://acme.example/about",
                "content": "Acme Manufacturing produces industrial equipment.",
            }
        ]
    )
    adapter = TavilyDirectoryAdapter(client=client, settings=CompanyResearchSettings())
    request = CompanyResearchRequest(geography="India")

    candidates = await adapter.discover(request)
    assert candidates == []


@pytest.mark.asyncio
async def test_discover_skips_blocked_domains():
    client = _client_returning(
        [
            {
                "title": "Manufacturing Directory",
                "url": "https://linkedin.com/directory",
                "content": _DIRECTORY_CONTENT,
            }
        ]
    )
    adapter = TavilyDirectoryAdapter(client=client, settings=CompanyResearchSettings())
    request = CompanyResearchRequest(geography="India")

    candidates = await adapter.discover(request)
    assert candidates == []


@pytest.mark.asyncio
async def test_discover_caches_results_across_calls():
    client = _client_returning([_DIRECTORY_RESULT])
    adapter = TavilyDirectoryAdapter(client=client, settings=CompanyResearchSettings())
    request = CompanyResearchRequest(geography="India", industries=["Manufacturing"])

    first = await adapter.discover(request)
    second = await adapter.discover(request)

    assert first == second
    client.search.assert_called()
    call_count_after_first_pass = client.search.call_count
    # A third call for the same request must not issue any new searches.
    await adapter.discover(request)
    assert client.search.call_count == call_count_after_first_pass


@pytest.mark.asyncio
async def test_discover_cache_key_differs_by_geography():
    client = _client_returning([_DIRECTORY_RESULT])
    adapter = TavilyDirectoryAdapter(client=client, settings=CompanyResearchSettings())

    await adapter.discover(CompanyResearchRequest(geography="India", industries=["Manufacturing"]))
    count_after_india = client.search.call_count

    await adapter.discover(CompanyResearchRequest(geography="Germany", industries=["Manufacturing"]))
    assert client.search.call_count > count_after_india


@pytest.mark.asyncio
async def test_discover_cache_expires_after_ttl():
    client = _client_returning([_DIRECTORY_RESULT])
    adapter = TavilyDirectoryAdapter(
        client=client, settings=CompanyResearchSettings(directory_cache_ttl_seconds=0)
    )
    request = CompanyResearchRequest(geography="India", industries=["Manufacturing"])

    await adapter.discover(request)
    count_after_first = client.search.call_count

    # TTL of 0 means any elapsed time invalidates the cache entry.
    await adapter.discover(request)
    assert client.search.call_count > count_after_first
