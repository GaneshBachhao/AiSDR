"""
Assembles the public ``CompanySearchResult`` DTO from the outputs of the
discovery -> identity verification -> evidence -> scoring pipeline.

This is pure assembly/text-generation logic with no I/O of its own, kept
separate from ``SearchCompaniesHandler`` so it can be unit tested directly
against fixed inputs.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.application.company_research.dto.company_research_request import (
    CompanyResearchRequest,
)
from app.application.company_research.dto.company_research_response import (
    CompanySearchResult,
    EvidenceItem,
)
from app.application.company_research.ports.identity_verification_port import (
    IdentityVerificationResult,
)
from app.domain.company_research.entities.candidate import CompanyCandidate
from app.domain.company_research.services.evidence_signal_extractor import (
    EvidenceSignalExtractor,
)
from app.domain.company_research.services.icp_matcher import IcpMatcher
from app.domain.company_research.services.opportunity_mapper import OpportunityMapper
from app.domain.company_research.value_objects.qualification_score import QualificationScore


@dataclass(slots=True)
class ResearchOutcome:
    """Everything the mapper needs to build one ``CompanySearchResult``."""

    candidate: CompanyCandidate
    identity: IdentityVerificationResult
    evidence: list[EvidenceItem]
    industry: str | None
    industry_reason: str
    employee_count: int | None
    icp_match: bool
    icp_match_reason: str
    score: QualificationScore
    evidence_classification: str
    signals: dict[str, bool] = field(default_factory=dict)


class CompanyResearchMapper:
    """Builds ``CompanySearchResult`` DTOs from a fully-researched candidate."""

    @classmethod
    def to_response(
        cls,
        outcome: ResearchOutcome,
        request: CompanyResearchRequest,
    ) -> CompanySearchResult:
        combined = " ".join((item.snippet or "") for item in outcome.evidence).lower()
        has_evidence = outcome.evidence_classification in (
            "Confirmed Need",
            "Strong Opportunity Signal",
        )

        opportunities, services = OpportunityMapper.map_signals(outcome.signals)
        problem = cls._problem_hypothesis(has_evidence)
        evidence_text = cls._evidence_text(has_evidence, outcome.signals)
        observation = cls._best_observation(outcome.evidence, outcome.signals)
        role = cls._select_buyer_role(request, services, outcome.signals)
        website = str(outcome.identity.verified_website) if outcome.identity.verified_website else None
        evidence_date = next((item.evidence_date for item in outcome.evidence if item.evidence_date), None)

        message = (
            f"Subject: A possible improvement opportunity at {outcome.candidate.company_name}\n\n"
            f"Hello,\n\nI was reviewing public information about {outcome.candidate.company_name} "
            f"and noticed {observation}. We help businesses with {', '.join(services[:2])}. "
            "There may be a practical opportunity to improve a related process or technology "
            "capability. If useful, I can share a short view of what we found and where there "
            "may be a fit. Would that be worth a brief discussion?\n\nRegards"
        )

        confidence = (
            "High"
            if len(outcome.evidence) >= 5 and has_evidence and outcome.industry_reason
            else "Medium"
            if outcome.evidence
            else "Low"
        )

        return CompanySearchResult(
            company_name=outcome.candidate.company_name,
            industry=outcome.industry,
            industry_match=True,
            industry_match_reason=outcome.industry_reason,
            location=cls._extract_location(combined, request.geography),
            website=website,
            company_size=IcpMatcher.company_size_label(outcome.employee_count),
            employee_count=outcome.employee_count,
            parent_company=outcome.identity.parent_company,
            icp_match=outcome.icp_match,
            icp_match_reason=outcome.icp_match_reason,
            business_description=cls._business_description(outcome.evidence, outcome.candidate.company_name),
            opportunity_type=opportunities,
            evidence_of_need=evidence_text,
            evidence_classification=outcome.evidence_classification,
            business_problem_hypothesis=problem,
            recommended_solution=services,
            expected_business_impact=(
                "Potential impact includes reduced manual effort, faster processing or "
                "reporting, improved integration, and better scalability."
            ),
            trigger_event=EvidenceSignalExtractor.trigger_event(outcome.signals),
            evidence_date=evidence_date,
            decision_maker_role=role,
            decision_maker_name=None,
            public_contact_channel=website,
            discovery_metadata=outcome.candidate.discovery_metadata,
            qualification_score=outcome.score.total,
            priority_tier=outcome.score.tier,
            recommended_outreach_angle=(
                f"Because {observation}, {outcome.candidate.company_name} may be worth reviewing "
                f"for a focused {services[0].lower()} opportunity."
            ),
            suggested_first_message=message,
            sources=outcome.evidence,
            confidence_level=confidence,
        )

    @staticmethod
    def _problem_hypothesis(has_evidence: bool) -> str:
        if has_evidence:
            return (
                "Public signals suggest there may be an opportunity to improve one or more "
                "technology, workflow, data, or reporting processes."
            )
        return (
            "A reasonable starting hypothesis is that the company may have room to improve an "
            "internal system, workflow, integration, or reporting process; this is not a "
            "confirmed requirement."
        )

    @staticmethod
    def _evidence_text(has_evidence: bool, signals: dict[str, bool]) -> str:
        if has_evidence:
            confirmed = [key for key, value in signals.items() if value]
            return (
                f"Public sources show company-specific signals related to {', '.join(confirmed)}. "
                "These signals support further qualification but do not prove an active buying "
                "requirement."
            )
        return (
            "No reliable public evidence was found for a specific technology requirement; the "
            "opportunity below is a hypothesis for human validation."
        )

    @staticmethod
    def _business_description(evidence: list[EvidenceItem], company_name: str) -> str | None:
        for item in evidence:
            snippet = (item.snippet or "").strip()
            if snippet and company_name.lower() in snippet.lower():
                return snippet[:500]
        return None

    @staticmethod
    def _best_observation(evidence: list[EvidenceItem], signals: dict[str, bool]) -> str:
        for item in evidence:
            snippet = (item.snippet or "").strip()
            if snippet:
                clean = " ".join(snippet.split())
                return clean[:240].rstrip(".,")
        confirmed = [key for key, value in signals.items() if value]
        return f"public information shows signals related to {', '.join(confirmed) if confirmed else 'technology or business improvement'}"

    @staticmethod
    def _extract_location(text: str, fallback: str | None = None) -> str | None:
        markers = ("headquartered in ", "headquarters in ", "based in ")
        lower = text.lower()
        for marker in markers:
            idx = lower.find(marker)
            if idx >= 0:
                value = text[idx + len(marker):].split(".")[0].strip()
                if 2 <= len(value) <= 100:
                    return value.title()
        return fallback

    @staticmethod
    def _select_buyer_role(
        request: CompanyResearchRequest,
        services: list[str],
        signals: dict[str, bool],
    ) -> str | None:
        preferred = list(request.preferred_decision_makers)
        if preferred:
            for role in preferred:
                upper = role.upper()
                if "CTO" in upper or "CIO" in upper or "COO" in upper:
                    return role
            return preferred[0]
        if "Business Process Automation" in services:
            return "COO / Operations Leader"
        if "Azure Modernization" in services or "Custom Application Development" in services:
            return "CTO / CIO"
        return "CTO / CIO / COO"
