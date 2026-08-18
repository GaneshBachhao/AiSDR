from __future__ import annotations

from unittest.mock import Mock

import pytest

from app.application.company_research.dto.company_research_request import (
    CompanyResearchRequest,
)
from app.application.company_research.ports.identity_verification_port import (
    IdentityVerificationResult,
)
from app.domain.company_research.entities.candidate import CompanyCandidate
from app.infrastructure.company_research.tavily_evidence_adapter import (
    TavilyEvidenceAdapter,
)
from app.infrastructure.configuration.company_research_settings import (
    CompanyResearchSettings,
)
from app.integrations.tavily.exceptions import TavilyRateLimitException


def _candidate() -> CompanyCandidate:
    return CompanyCandidate(
        company_name="Acme Manufacturing",
        website="https://acme.example",
        title="Acme Manufacturing",
        content="",
        source_url="https://acme.example",
    )


def _identity() -> IdentityVerificationResult:
    return IdentityVerificationResult(
        verified_website="https://acme.example", confidence="HIGH", parent_company=None, reason="matched"
    )


@pytest.mark.asyncio
async def test_gather_returns_evidence_items_from_search_results():
    client = Mock()
    client.search.return_value = [
        {
            "title": "Acme is hiring cloud engineers",
            "url": "https://acme.example/careers",
            "content": "Acme Manufacturing is hiring cloud and automation engineers.",
            "published_date": "2026-01-01",
        }
    ]
    adapter = TavilyEvidenceAdapter(client=client, settings=CompanyResearchSettings())
    request = CompanyResearchRequest(geography="India")

    evidence = await adapter.gather(_candidate(), _identity(), request)

    assert len(evidence) >= 1
    assert evidence[0].title == "Acme is hiring cloud engineers"
    assert evidence[0].evidence_date == "2026-01-01"
    assert evidence[0].observed_date is not None
    assert evidence[0].signal_scope == "company_specific"


@pytest.mark.asyncio
async def test_gather_tags_evidence_without_the_company_name_as_industry_general():
    client = Mock()
    client.search.return_value = [
        {
            "title": "Manufacturing sector sees rising automation investment",
            "url": "https://industry-news.example/article",
            "content": "The broader manufacturing sector is investing heavily in automation.",
        }
    ]
    adapter = TavilyEvidenceAdapter(client=client, settings=CompanyResearchSettings())
    request = CompanyResearchRequest(geography="India")

    evidence = await adapter.gather(_candidate(), _identity(), request)

    assert len(evidence) == 1
    assert evidence[0].signal_scope == "industry_general"


@pytest.mark.asyncio
async def test_gather_deduplicates_urls_across_queries():
    client = Mock()
    client.search.return_value = [{"title": "Acme", "url": "https://acme.example/page", "content": "x"}]
    adapter = TavilyEvidenceAdapter(client=client, settings=CompanyResearchSettings())
    request = CompanyResearchRequest(geography="India")

    evidence = await adapter.gather(_candidate(), _identity(), request)
    urls = [str(item.url) for item in evidence]
    assert len(urls) == len(set(urls))


@pytest.mark.asyncio
async def test_gather_skips_blocked_domains():
    client = Mock()
    client.search.return_value = [
        {"title": "Acme on LinkedIn", "url": "https://linkedin.com/company/acme", "content": "x"}
    ]
    adapter = TavilyEvidenceAdapter(client=client, settings=CompanyResearchSettings())
    request = CompanyResearchRequest(geography="India")

    evidence = await adapter.gather(_candidate(), _identity(), request)
    assert evidence == []


@pytest.mark.asyncio
async def test_gather_degrades_gracefully_when_one_query_is_rate_limited(caplog):
    """A rate limit on one of the 2-3 evidence queries must not crash the
    whole candidate -- fewer evidence items just means lower scoring
    downstream, not a hard failure (unlike identity verification)."""
    client = Mock()
    client.search.side_effect = [
        TavilyRateLimitException("Tavily usage limit exceeded"),
        [{"title": "Acme funding", "url": "https://acme.example/news", "content": "Acme raised funding."}],
    ]
    adapter = TavilyEvidenceAdapter(client=client, settings=CompanyResearchSettings())
    request = CompanyResearchRequest(geography="India")

    with caplog.at_level("WARNING"):
        evidence = await adapter.gather(_candidate(), _identity(), request)

    assert len(evidence) == 1
    assert evidence[0].title == "Acme funding"
    assert "RATE_LIMIT" in caplog.text


@pytest.mark.asyncio
async def test_gather_respects_max_evidence_items_setting():
    client = Mock()
    client.search.return_value = [
        {"title": f"Item {i}", "url": f"https://acme.example/{i}", "content": "signal"} for i in range(10)
    ]
    adapter = TavilyEvidenceAdapter(client=client, settings=CompanyResearchSettings(max_evidence_items=3))
    request = CompanyResearchRequest(geography="India")

    evidence = await adapter.gather(_candidate(), _identity(), request)
    assert len(evidence) <= 3
