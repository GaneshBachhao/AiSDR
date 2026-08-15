from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from app.infrastructure.ai.exceptions.ai_budget_exceeded_exception import (
    AIBudgetExceededException,
)
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


def _scoped_evidence(name: str, scope: str, count: int) -> list[EvidenceItem]:
    slug = name.lower().replace(" ", "-")
    snippets = [
        f"{name} is hiring cloud and software engineers as part of a technology modernization push.",
        f"{name} announced a major expansion and a new funding round.",
        "The broader industry sector is seeing growth in automation investment.",
    ]
    return [
        EvidenceItem(
            title=f"Evidence {i}",
            url=f"https://{slug}.example/{i}",
            snippet=snippets[i % len(snippets)],
            signal_scope=scope,
        )
        for i in range(count)
    ]


@pytest.mark.asyncio
async def test_confirmed_need_reachable_with_company_specific_evidence():
    candidate = _candidate("Acme Manufacturing", "https://acme.example")
    handler = SearchCompaniesHandler(
        ScriptedDiscoveryAdapter([candidate]),
        ScriptedIdentityAdapter({"Acme Manufacturing": _verified("https://acme.example")}),
        ScriptedEvidenceAdapter(
            {"Acme Manufacturing": _scoped_evidence("Acme Manufacturing", "company_specific", 3)}
        ),
    )
    request = CompanyResearchRequest(geography="India")
    results = await handler.handle(request)
    assert len(results) == 1
    assert results[0].evidence_classification == "Confirmed Need"


@pytest.mark.asyncio
async def test_confirmed_need_unreachable_with_only_industry_general_evidence():
    """Regression guard, end-to-end: industry-general evidence -- even with
    plenty of signal keywords and enough items -- must never classify as
    Confirmed Need."""
    candidate = _candidate("Acme Manufacturing", "https://acme.example")
    handler = SearchCompaniesHandler(
        ScriptedDiscoveryAdapter([candidate]),
        ScriptedIdentityAdapter({"Acme Manufacturing": _verified("https://acme.example")}),
        ScriptedEvidenceAdapter(
            {"Acme Manufacturing": _scoped_evidence("Acme Manufacturing", "industry_general", 3)}
        ),
    )
    request = CompanyResearchRequest(geography="India")
    results = await handler.handle(request)
    assert len(results) == 1
    assert results[0].evidence_classification != "Confirmed Need"


@pytest.mark.asyncio
async def test_budget_guard_checked_with_accepted_candidate_count_before_any_ai_call():
    candidates = [_candidate("Acme A", "https://a.example"), _candidate("Acme B", "https://b.example")]
    identity_adapter = AsyncMock(spec=IdentityVerificationPort)
    identity_adapter.verify.return_value = _verified("https://a.example")
    budget_guard = AsyncMock()

    handler = SearchCompaniesHandler(
        ScriptedDiscoveryAdapter(candidates),
        identity_adapter,
        ScriptedEvidenceAdapter({}),
        budget_port=budget_guard,
        ai_provider_name="gemini",
    )
    request = CompanyResearchRequest(geography="India")

    await handler.handle(request)

    budget_guard.ensure_batch_fits.assert_awaited_once_with("gemini", 2)


@pytest.mark.asyncio
async def test_budget_exceeded_prevents_any_identity_verification_call():
    candidates = [_candidate("Acme A", "https://a.example")]
    identity_adapter = AsyncMock(spec=IdentityVerificationPort)
    budget_guard = AsyncMock()
    budget_guard.ensure_batch_fits.side_effect = AIBudgetExceededException("budget exceeded")

    handler = SearchCompaniesHandler(
        ScriptedDiscoveryAdapter(candidates),
        identity_adapter,
        ScriptedEvidenceAdapter({}),
        budget_port=budget_guard,
        ai_provider_name="gemini",
    )
    request = CompanyResearchRequest(geography="India")

    with pytest.raises(AIBudgetExceededException):
        await handler.handle(request)

    identity_adapter.verify.assert_not_awaited()


@pytest.mark.asyncio
async def test_no_budget_guard_configured_skips_check_entirely():
    candidate = _candidate("Acme Manufacturing", "https://acme.example")
    handler = SearchCompaniesHandler(
        ScriptedDiscoveryAdapter([candidate]),
        ScriptedIdentityAdapter({"Acme Manufacturing": _verified("https://acme.example")}),
        ScriptedEvidenceAdapter({"Acme Manufacturing": _hiring_evidence("Acme Manufacturing")}),
        # no budget_port / ai_provider_name -- must behave exactly as before
    )
    request = CompanyResearchRequest(geography="India", industries=["Manufacturing"])
    results = await handler.handle(request)
    assert len(results) == 1


@pytest.mark.asyncio
async def test_no_directory_port_configured_uses_only_discovery_port():
    """Regression guard: omitting directory_port must behave exactly as
    before the cheap tier existed."""
    candidate = _candidate("Acme Manufacturing", "https://acme.example")
    discovery = AsyncMock(spec=CompanyDiscoveryPort)
    discovery.discover.return_value = [candidate]

    handler = SearchCompaniesHandler(
        discovery,
        ScriptedIdentityAdapter({"Acme Manufacturing": _verified("https://acme.example")}),
        ScriptedEvidenceAdapter({"Acme Manufacturing": _hiring_evidence("Acme Manufacturing")}),
        # no directory_port
    )
    request = CompanyResearchRequest(geography="India", industries=["Manufacturing"])
    results = await handler.handle(request)

    assert len(results) == 1
    discovery.discover.assert_awaited_once_with(request)


@pytest.mark.asyncio
async def test_cheap_tier_alone_used_when_it_fills_the_pool():
    candidates = [
        _candidate("Acme A", "https://a.example"),
        _candidate("Acme B", "https://b.example"),
    ]
    directory = AsyncMock()
    directory.discover.return_value = candidates
    discovery = AsyncMock(spec=CompanyDiscoveryPort)

    handler = SearchCompaniesHandler(
        discovery,
        ScriptedIdentityAdapter(
            {"Acme A": _verified("https://a.example"), "Acme B": _verified("https://b.example")}
        ),
        ScriptedEvidenceAdapter({}),
        directory_port=directory,
    )
    request = CompanyResearchRequest(geography="India", number_of_companies=2)
    await handler.handle(request)

    directory.discover.assert_awaited_once_with(request)
    discovery.discover.assert_not_awaited()


@pytest.mark.asyncio
async def test_falls_back_to_expensive_tier_when_cheap_tier_is_insufficient():
    cheap_candidate = _candidate("Acme A", "https://a.example")
    expensive_candidate = _candidate("Acme B", "https://b.example")

    directory = AsyncMock()
    directory.discover.return_value = [cheap_candidate]
    discovery = AsyncMock(spec=CompanyDiscoveryPort)
    discovery.discover.return_value = [expensive_candidate]

    handler = SearchCompaniesHandler(
        discovery,
        ScriptedIdentityAdapter(
            {"Acme A": _verified("https://a.example"), "Acme B": _verified("https://b.example")}
        ),
        ScriptedEvidenceAdapter({}),
        directory_port=directory,
    )
    # Requesting more companies than the cheap tier alone can supply.
    request = CompanyResearchRequest(geography="India", number_of_companies=5)
    results = await handler.handle(request)

    directory.discover.assert_awaited_once_with(request)
    discovery.discover.assert_awaited_once_with(request)
    assert {r.company_name for r in results} == {"Acme A", "Acme B"}


@pytest.mark.asyncio
async def test_persist_as_companies_false_never_calls_the_promoter():
    candidate = _candidate("Acme Manufacturing", "https://acme.example")
    promoter = AsyncMock()
    handler = SearchCompaniesHandler(
        ScriptedDiscoveryAdapter([candidate]),
        ScriptedIdentityAdapter({"Acme Manufacturing": _verified("https://acme.example")}),
        ScriptedEvidenceAdapter({"Acme Manufacturing": _hiring_evidence("Acme Manufacturing")}),
        candidate_promoter=promoter,
    )
    request = CompanyResearchRequest(geography="India", industries=["Manufacturing"])
    # persist_as_companies defaults to False.
    results = await handler.handle(request)

    promoter.handle.assert_not_awaited()
    assert results[0].persisted_company_id is None


@pytest.mark.asyncio
async def test_persist_as_companies_true_promotes_each_final_result():
    candidate = _candidate("Acme Manufacturing", "https://acme.example")
    promoter = AsyncMock()
    promoter.handle.return_value = "company-123"
    handler = SearchCompaniesHandler(
        ScriptedDiscoveryAdapter([candidate]),
        ScriptedIdentityAdapter({"Acme Manufacturing": _verified("https://acme.example")}),
        ScriptedEvidenceAdapter({"Acme Manufacturing": _hiring_evidence("Acme Manufacturing")}),
        candidate_promoter=promoter,
    )
    request = CompanyResearchRequest(
        geography="India", industries=["Manufacturing"], persist_as_companies=True
    )
    results = await handler.handle(request)

    promoter.handle.assert_awaited_once()
    assert results[0].persisted_company_id == "company-123"


@pytest.mark.asyncio
async def test_persist_as_companies_true_without_a_promoter_configured_is_a_noop():
    candidate = _candidate("Acme Manufacturing", "https://acme.example")
    handler = SearchCompaniesHandler(
        ScriptedDiscoveryAdapter([candidate]),
        ScriptedIdentityAdapter({"Acme Manufacturing": _verified("https://acme.example")}),
        ScriptedEvidenceAdapter({"Acme Manufacturing": _hiring_evidence("Acme Manufacturing")}),
        # no candidate_promoter configured
    )
    request = CompanyResearchRequest(
        geography="India", industries=["Manufacturing"], persist_as_companies=True
    )
    results = await handler.handle(request)

    assert len(results) == 1
    assert results[0].persisted_company_id is None


@pytest.mark.asyncio
async def test_promotion_failure_does_not_break_the_research_response():
    candidate = _candidate("Acme Manufacturing", "https://acme.example")
    promoter = AsyncMock()
    promoter.handle.side_effect = RuntimeError("db unavailable")
    handler = SearchCompaniesHandler(
        ScriptedDiscoveryAdapter([candidate]),
        ScriptedIdentityAdapter({"Acme Manufacturing": _verified("https://acme.example")}),
        ScriptedEvidenceAdapter({"Acme Manufacturing": _hiring_evidence("Acme Manufacturing")}),
        candidate_promoter=promoter,
    )
    request = CompanyResearchRequest(
        geography="India", industries=["Manufacturing"], persist_as_companies=True
    )
    results = await handler.handle(request)

    assert len(results) == 1
    assert results[0].persisted_company_id is None
