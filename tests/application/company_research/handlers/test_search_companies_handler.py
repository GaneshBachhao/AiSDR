from __future__ import annotations

import pytest

from app.application.company_research.dto.company_research_request import (
    CompanyResearchRequest,
)
from app.application.company_research.dto.company_research_response import EvidenceItem
from app.application.company_research.handlers.search_companies_handler import (
    SearchCompaniesHandler,
)
from app.application.company_research.ports.company_discovery_port import (
    CompanyDiscoveryPort,
)
from app.application.company_research.ports.evidence_research_port import (
    EvidenceResearchPort,
)
from app.application.company_research.ports.identity_verification_port import (
    IdentityVerificationPort,
    IdentityVerificationResult,
)
from app.domain.company_research.entities.candidate import CompanyCandidate


def _candidate(name: str, website: str) -> CompanyCandidate:
    return CompanyCandidate(
        company_name=name,
        website=website,
        title=f"{name} | Official Site",
        content=f"{name} is a manufacturer of industrial equipment with approximately 120 employees.",
        source_url=website,
    )


class ScriptedDiscoveryAdapter(CompanyDiscoveryPort):
    def __init__(self, candidates: list[CompanyCandidate]) -> None:
        self._candidates = candidates

    async def discover(self, request):
        return self._candidates


class ScriptedIdentityAdapter(IdentityVerificationPort):
    def __init__(self, results: dict[str, IdentityVerificationResult]) -> None:
        self._results = results

    async def verify(self, candidate):
        return self._results[candidate.company_name]


class ScriptedEvidenceAdapter(EvidenceResearchPort):
    def __init__(self, evidence_by_name: dict[str, list[EvidenceItem]]) -> None:
        self._evidence_by_name = evidence_by_name

    async def gather(self, candidate, identity, request):
        return self._evidence_by_name.get(candidate.company_name, [])


class PartiallyFailingEvidenceAdapter(EvidenceResearchPort):
    """Fails for a named candidate, succeeds with hiring evidence for everyone else."""

    def __init__(self, failing_name: str) -> None:
        self._failing_name = failing_name

    async def gather(self, candidate, identity, request):
        if candidate.company_name == self._failing_name:
            raise RuntimeError("evidence source unavailable")
        return _hiring_evidence(candidate.company_name)


def _hiring_evidence(name: str) -> list[EvidenceItem]:
    slug = name.lower().replace(" ", "-")
    return [
        EvidenceItem(
            title=f"{name} hiring",
            url=f"https://{slug}.example/careers",
            snippet=f"{name} is hiring cloud and technology roles amid rapid growth.",
            evidence_date=None,
        )
    ]


def _verified(website: str) -> IdentityVerificationResult:
    return IdentityVerificationResult(
        verified_website=website, confidence="HIGH", parent_company=None, reason="matched"
    )


def _unverified() -> IdentityVerificationResult:
    return IdentityVerificationResult(
        verified_website=None, confidence="LOW", parent_company=None, reason="identity_not_verified"
    )


@pytest.mark.asyncio
async def test_returns_empty_list_when_discovery_finds_nothing():
    handler = SearchCompaniesHandler(
        ScriptedDiscoveryAdapter([]),
        ScriptedIdentityAdapter({}),
        ScriptedEvidenceAdapter({}),
    )
    request = CompanyResearchRequest(geography="India")
    assert await handler.handle(request) == []


@pytest.mark.asyncio
async def test_rejects_candidate_with_unverified_identity():
    candidate = _candidate("Lathangi Motors", "https://tatamotors.com")
    handler = SearchCompaniesHandler(
        ScriptedDiscoveryAdapter([candidate]),
        ScriptedIdentityAdapter({"Lathangi Motors": _unverified()}),
        ScriptedEvidenceAdapter({}),
    )
    request = CompanyResearchRequest(geography="India")
    results = await handler.handle(request)
    assert results == []


@pytest.mark.asyncio
async def test_verified_candidate_with_evidence_is_returned():
    candidate = _candidate("Acme Manufacturing", "https://acme.example")
    handler = SearchCompaniesHandler(
        ScriptedDiscoveryAdapter([candidate]),
        ScriptedIdentityAdapter({"Acme Manufacturing": _verified("https://acme.example")}),
        ScriptedEvidenceAdapter({"Acme Manufacturing": _hiring_evidence("Acme Manufacturing")}),
    )
    request = CompanyResearchRequest(geography="India", industries=["Manufacturing"], number_of_companies=5)
    results = await handler.handle(request)
    assert len(results) == 1
    assert results[0].company_name == "Acme Manufacturing"
    assert results[0].qualification_score > 0


@pytest.mark.asyncio
async def test_industry_mismatch_is_rejected():
    candidate = CompanyCandidate(
        company_name="Acme Bakery",
        website="https://acmebakery.example",
        title="Acme Bakery",
        content="Acme Bakery sells fresh bread and pastries.",
        source_url="https://acmebakery.example",
    )
    handler = SearchCompaniesHandler(
        ScriptedDiscoveryAdapter([candidate]),
        ScriptedIdentityAdapter({"Acme Bakery": _verified("https://acmebakery.example")}),
        ScriptedEvidenceAdapter({}),
    )
    request = CompanyResearchRequest(geography="India", industries=["Manufacturing"])
    results = await handler.handle(request)
    assert results == []


@pytest.mark.asyncio
async def test_company_size_gate_rejects_unknown_employee_count():
    candidate = CompanyCandidate(
        company_name="Acme Manufacturing",
        website="https://acme.example",
        title="Acme Manufacturing",
        content="Acme Manufacturing produces industrial equipment.",
        source_url="https://acme.example",
    )
    handler = SearchCompaniesHandler(
        ScriptedDiscoveryAdapter([candidate]),
        ScriptedIdentityAdapter({"Acme Manufacturing": _verified("https://acme.example")}),
        ScriptedEvidenceAdapter({}),
    )
    request = CompanyResearchRequest(geography="India", company_size=["SMB"])
    results = await handler.handle(request)
    assert results == []


@pytest.mark.asyncio
async def test_minimum_qualification_score_filters_low_scoring_results():
    candidate = _candidate("Acme Manufacturing", "https://acme.example")
    handler = SearchCompaniesHandler(
        ScriptedDiscoveryAdapter([candidate]),
        ScriptedIdentityAdapter({"Acme Manufacturing": _verified("https://acme.example")}),
        ScriptedEvidenceAdapter({}),
    )
    request = CompanyResearchRequest(geography="India", minimum_qualification_score=95)
    results = await handler.handle(request)
    assert results == []


@pytest.mark.asyncio
async def test_results_sorted_and_truncated_to_number_of_companies():
    candidates = [_candidate("Acme A", "https://a.example"), _candidate("Acme B", "https://b.example")]
    handler = SearchCompaniesHandler(
        ScriptedDiscoveryAdapter(candidates),
        ScriptedIdentityAdapter(
            {"Acme A": _verified("https://a.example"), "Acme B": _verified("https://b.example")}
        ),
        ScriptedEvidenceAdapter(
            {"Acme A": _hiring_evidence("Acme A"), "Acme B": []}
        ),
    )
    request = CompanyResearchRequest(geography="India", number_of_companies=1)
    results = await handler.handle(request)
    assert len(results) == 1
    assert results[0].company_name == "Acme A"


@pytest.mark.asyncio
async def test_one_candidate_failure_does_not_break_others():
    candidates = [_candidate("Acme A", "https://a.example"), _candidate("Acme B", "https://b.example")]
    handler = SearchCompaniesHandler(
        ScriptedDiscoveryAdapter(candidates),
        ScriptedIdentityAdapter(
            {"Acme A": _verified("https://a.example"), "Acme B": _verified("https://b.example")}
        ),
        PartiallyFailingEvidenceAdapter(failing_name="Acme A"),
    )
    request = CompanyResearchRequest(geography="India")
    results = await handler.handle(request)
    assert [r.company_name for r in results] == ["Acme B"]
