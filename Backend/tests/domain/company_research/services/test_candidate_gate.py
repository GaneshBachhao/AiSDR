"""Dedicated tests for DeterministicCandidateGate (EPIC-17).

No dedicated test file existed for this class before -- its only coverage
was incidental, inside test_discovery_funnel.py. This file closes that gap
and adds regression coverage for two real known-bad candidates observed in
live testing ("Company search", "Browse by size: 51-200 employees" --
docs/pamacore_aisdr_summary.md), which the gate did not reject before this
sprint's blocked_name_markers addition.
"""

from __future__ import annotations

from app.domain.company_research.entities.candidate import CompanyCandidate
from app.domain.company_research.services.candidate_gate import DeterministicCandidateGate


def candidate(name: str, url: str, title: str | None = None) -> CompanyCandidate:
    return CompanyCandidate(
        company_name=name,
        website=url,
        title=title or name,
        content="company information",
        source_url=url,
    )


def test_rejects_a_real_known_bad_candidate_company_search() -> None:
    gate = DeterministicCandidateGate()
    item = candidate("Company search", "https://listings.example/results", title="Search page")

    decision = gate.evaluate(item)

    assert decision.accepted is False
    assert decision.reason == "non_company_result_name"


def test_rejects_a_real_known_bad_candidate_browse_by_size() -> None:
    gate = DeterministicCandidateGate()
    item = candidate(
        "Browse by size: 51-200 employees",
        "https://listings.example/filters",
        title="Filter options",
    )

    decision = gate.evaluate(item)

    assert decision.accepted is False
    assert decision.reason == "non_company_result_name"


def test_accepts_a_normal_company_candidate() -> None:
    gate = DeterministicCandidateGate()
    item = candidate("Acme Manufacturing", "https://acme.example")

    decision = gate.evaluate(item)

    assert decision.accepted is True
    assert decision.reason == "accepted"


def test_rejects_missing_company_name() -> None:
    gate = DeterministicCandidateGate()
    item = candidate("   ", "https://acme.example")

    decision = gate.evaluate(item)

    assert decision.accepted is False
    assert decision.reason == "missing_company_name"


def test_rejects_missing_url() -> None:
    gate = DeterministicCandidateGate()
    item = CompanyCandidate(
        company_name="Acme",
        website=None,
        title="Acme",
        content="",
        source_url="",
    )

    decision = gate.evaluate(item)

    assert decision.accepted is False
    assert decision.reason == "missing_url"


def test_rejects_a_blocked_domain() -> None:
    gate = DeterministicCandidateGate()
    item = candidate("Acme on LinkedIn", "https://www.linkedin.com/company/acme")

    decision = gate.evaluate(item)

    assert decision.accepted is False
    assert decision.reason == "blocked_domain"


def test_rejects_a_blocked_document_extension() -> None:
    gate = DeterministicCandidateGate()
    item = candidate("Acme Report", "https://acme.example/brochure.pdf")

    decision = gate.evaluate(item)

    assert decision.accepted is False
    assert decision.reason == "blocked_document"


def test_rejects_a_blocked_title_marker() -> None:
    gate = DeterministicCandidateGate()
    item = candidate("Manufacturing Roundup", "https://acme.example", title="Top 10 Manufacturing Companies")

    decision = gate.evaluate(item)

    assert decision.accepted is False
    assert decision.reason == "non_company_result_title"


def test_rejects_name_outside_length_bounds() -> None:
    gate = DeterministicCandidateGate()
    too_short = candidate("Ab", "https://ab.example")
    too_long = candidate("A" * 121, "https://long.example")

    assert gate.evaluate(too_short).reason == "invalid_company_name_length"
    assert gate.evaluate(too_long).reason == "invalid_company_name_length"


def test_custom_blocked_name_markers_override_the_defaults() -> None:
    gate = DeterministicCandidateGate(blocked_name_markers=("custom junk",))
    still_blocked_by_default = candidate("Company search", "https://acme.example")
    blocked_by_custom_rule = candidate("Custom Junk Result", "https://acme.example")

    # A custom marker list replaces the defaults entirely, matching how
    # blocked_title_markers/blocked_domains already behave.
    assert gate.evaluate(still_blocked_by_default).accepted is True
    assert gate.evaluate(blocked_by_custom_rule).reason == "non_company_result_name"


def test_accept_unique_deduplicates_by_canonical_domain() -> None:
    gate = DeterministicCandidateGate()
    candidates = [
        candidate("Acme", "https://www.acme.example/path"),
        candidate("Acme Manufacturing", "https://acme.example/about"),
    ]

    accepted = gate.accept_unique(candidates)

    assert len(accepted) == 1


def test_accept_unique_skips_rejected_candidates() -> None:
    gate = DeterministicCandidateGate()
    candidates = [
        candidate("Company search", "https://directory.example/results"),
        candidate("Acme Manufacturing", "https://acme.example"),
    ]

    accepted = gate.accept_unique(candidates)

    assert [item.company_name for item in accepted] == ["Acme Manufacturing"]
