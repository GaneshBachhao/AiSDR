from __future__ import annotations

from unittest.mock import Mock

import pytest

from app.domain.company_research.entities.candidate import CompanyCandidate
from app.infrastructure.company_research.tavily_contact_discovery_adapter import (
    TavilyContactDiscoveryAdapter,
)
from app.infrastructure.configuration.company_research_settings import (
    CompanyResearchSettings,
)


def _candidate() -> CompanyCandidate:
    return CompanyCandidate(
        company_name="Acme Manufacturing",
        website="https://acme.example",
        title="Acme Manufacturing",
        content="",
        source_url="https://acme.example",
    )


@pytest.mark.asyncio
async def test_discover_parses_name_and_title_from_linkedin_result():
    client = Mock()
    client.search.return_value = [
        {
            "title": "John Smith - Chief Operating Officer - Acme Manufacturing | LinkedIn",
            "url": "https://linkedin.com/in/johnsmith",
        }
    ]
    adapter = TavilyContactDiscoveryAdapter(client=client, settings=CompanyResearchSettings())

    contacts = await adapter.discover(_candidate(), "https://acme.example", "COO / Operations Leader")

    assert len(contacts) == 1
    assert contacts[0].name == "John Smith"
    assert contacts[0].role_title == "Chief Operating Officer"
    assert str(contacts[0].linkedin_url) == "https://linkedin.com/in/johnsmith"


@pytest.mark.asyncio
async def test_discover_ignores_non_linkedin_profile_results():
    client = Mock()
    client.search.return_value = [
        {"title": "Acme Manufacturing - Wikipedia", "url": "https://en.wikipedia.org/wiki/Acme"},
        {"title": "Acme Manufacturing company page", "url": "https://linkedin.com/company/acme"},
    ]
    adapter = TavilyContactDiscoveryAdapter(client=client, settings=CompanyResearchSettings())

    contacts = await adapter.discover(_candidate(), "https://acme.example", None)

    assert contacts == []


@pytest.mark.asyncio
async def test_discover_deduplicates_the_same_person_across_queries():
    client = Mock()
    client.search.return_value = [
        {"title": "John Smith - COO - Acme | LinkedIn", "url": "https://linkedin.com/in/johnsmith"}
    ]
    adapter = TavilyContactDiscoveryAdapter(client=client, settings=CompanyResearchSettings())

    contacts = await adapter.discover(_candidate(), "https://acme.example", None)

    # Two queries are issued per discover() call; the same profile from both
    # must collapse into a single contact.
    assert len(contacts) == 1


@pytest.mark.asyncio
async def test_discover_respects_max_contacts_per_candidate_setting():
    client = Mock()
    client.search.return_value = [
        {"title": f"Person {i} - VP - Acme | LinkedIn", "url": f"https://linkedin.com/in/person{i}"}
        for i in range(10)
    ]
    adapter = TavilyContactDiscoveryAdapter(
        client=client, settings=CompanyResearchSettings(max_contacts_per_candidate=2)
    )

    contacts = await adapter.discover(_candidate(), "https://acme.example", None)

    assert len(contacts) <= 2


@pytest.mark.asyncio
async def test_discover_returns_empty_list_when_no_profile_found():
    client = Mock()
    client.search.return_value = []
    adapter = TavilyContactDiscoveryAdapter(client=client, settings=CompanyResearchSettings())

    contacts = await adapter.discover(_candidate(), "https://acme.example", "COO")

    assert contacts == []


def test_parse_person_and_title_rejects_titles_that_are_not_a_person_name():
    result = TavilyContactDiscoveryAdapter._parse_person_and_title(
        "Top 10 Manufacturing Companies in India | LinkedIn"
    )
    assert result is None


def test_parse_person_and_title_handles_name_only_titles():
    result = TavilyContactDiscoveryAdapter._parse_person_and_title("Jane Doe | LinkedIn")
    assert result == ("Jane Doe", None)
