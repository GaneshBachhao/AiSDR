from app.application.company_research.company_research_mapper import (
    CompanyResearchMapper,
    ResearchOutcome,
)
from app.application.company_research.dto.company_research_request import (
    CompanyResearchRequest,
)
from app.application.company_research.dto.company_research_response import EvidenceItem
from app.application.company_research.ports.identity_verification_port import (
    IdentityVerificationResult,
)
from app.domain.company_research.entities.candidate import CompanyCandidate
from app.domain.company_research.value_objects.qualification_score import QualificationScore


def _outcome(**overrides):
    defaults = dict(
        candidate=CompanyCandidate(
            company_name="Acme Manufacturing",
            website="https://acme.example",
            title="Acme Manufacturing",
            content="Acme Manufacturing produces industrial equipment.",
            source_url="https://acme.example",
        ),
        identity=IdentityVerificationResult(
            verified_website="https://acme.example",
            confidence="HIGH",
            parent_company=None,
            reason="matched",
        ),
        evidence=[
            EvidenceItem(
                title="Acme hiring cloud engineers",
                url="https://acme.example/careers",
                snippet="Acme Manufacturing is hiring cloud engineers and expanding operations.",
                evidence_date="2026-01-01",
            )
        ],
        industry="Manufacturing",
        industry_reason="Primary industry is consistent with requested industry: manufacturing.",
        employee_count=120,
        icp_match=True,
        icp_match_reason="Verified employee count 120 matches the requested company-size range.",
        score=QualificationScore(
            business_fit=23, evidence_strength=22, buying_signal=17, ability=12, accessibility=9
        ),
        evidence_classification="Strong Opportunity Signal",
        signals={
            "hiring": True,
            "growth": True,
            "technology": False,
            "ai": False,
            "process": False,
            "funding": False,
        },
    )
    defaults.update(overrides)
    return ResearchOutcome(**defaults)


def _request(**overrides):
    defaults = dict(geography="India", industries=["Manufacturing"], number_of_companies=5)
    defaults.update(overrides)
    return CompanyResearchRequest(**defaults)


def test_to_response_carries_core_identity_fields():
    result = CompanyResearchMapper.to_response(_outcome(), _request())
    assert result.company_name == "Acme Manufacturing"
    assert str(result.website).startswith("https://acme.example")
    assert result.qualification_score == 83
    assert result.priority_tier == "Tier A"
    assert result.evidence_classification == "Strong Opportunity Signal"


def test_to_response_website_is_none_when_identity_unverified():
    outcome = _outcome(
        identity=IdentityVerificationResult(
            verified_website=None, confidence="LOW", parent_company=None, reason="unverified"
        )
    )
    result = CompanyResearchMapper.to_response(outcome, _request())
    assert result.website is None
    assert result.public_contact_channel is None


def test_to_response_trigger_event_reflects_signals():
    result = CompanyResearchMapper.to_response(_outcome(), _request())
    assert result.trigger_event == "technology hiring, growth / expansion"


def test_to_response_parent_company_passed_through():
    outcome = _outcome(
        identity=IdentityVerificationResult(
            verified_website="https://acme.example",
            confidence="HIGH",
            parent_company="Example Holdings",
            reason="matched",
        )
    )
    result = CompanyResearchMapper.to_response(outcome, _request())
    assert result.parent_company == "Example Holdings"


def test_to_response_message_includes_company_name():
    result = CompanyResearchMapper.to_response(_outcome(), _request())
    assert "Acme Manufacturing" in result.suggested_first_message
    assert result.suggested_first_message.startswith("Subject:")


def test_to_response_surfaces_evidence_signals():
    """
    EPIC-12: the signals dict was already computed and used for scoring
    but previously discarded before reaching CompanySearchResult -- it
    must now survive into the response so a persisted Lead can carry it.
    """
    result = CompanyResearchMapper.to_response(_outcome(), _request())
    assert result.evidence_signals == {
        "hiring": True,
        "growth": True,
        "technology": False,
        "ai": False,
        "process": False,
        "funding": False,
    }
