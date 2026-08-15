"""
Search Companies application handler.

Orchestrates the full research pipeline: discover -> deterministic gate ->
identity verification -> evidence gathering -> deterministic classification
and scoring -> response assembly. This is a stateless research operation by
default -- ports injected via the constructor, no ``UnitOfWork`` of its own,
shaped like ``AIExecutionService`` rather than the repository-backed CQRS
handlers used by persisted CRM aggregates. The one exception is opt-in:
when ``CompanyResearchRequest.persist_as_companies`` is set, results are
additionally resolved/created as real Company records via
``PromoteCandidateToCompanyHandler`` (which does own a ``UnitOfWork``).
"""

from __future__ import annotations

import asyncio
import logging

from app.application.company_research.company_research_mapper import (
    CompanyResearchMapper,
    ResearchOutcome,
)
from app.application.company_research.dto.company_research_request import (
    CompanyResearchRequest,
)
from app.application.company_research.dto.company_research_response import (
    CompanySearchResult,
)
from app.application.company_research.handlers.promote_candidate_to_company_handler import (
    PromoteCandidateToCompanyHandler,
)
from app.application.company_research.ports.company_directory_port import (
    CompanyDirectoryPort,
)
from app.application.company_research.ports.company_discovery_port import (
    CompanyDiscoveryPort,
)
from app.application.company_research.ports.evidence_research_port import (
    EvidenceResearchPort,
)
from app.application.company_research.ports.identity_verification_port import (
    IdentityVerificationPort,
)
from app.application.ai.ports.ai_budget_port import AIBudgetPort
from app.domain.company_research.entities.candidate import CompanyCandidate
from app.domain.company_research.services.discovery_funnel import DiscoveryFunnel
from app.domain.company_research.services.evidence_signal_extractor import (
    EvidenceSignalExtractor,
)
from app.domain.company_research.services.icp_matcher import IcpMatcher
from app.domain.company_research.services.industry_classifier import IndustryClassifier
from app.domain.company_research.services.opportunity_mapper import OpportunityMapper
from app.domain.recommendation.value_objects.solution_catalog_entry import (
    SolutionCatalogEntry,
)
from app.domain.company_research.services.qualification_scorer import (
    QualificationScorer,
    ScoringInputs,
)

logger = logging.getLogger(__name__)

_CONFIDENCE_RANK = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}


class SearchCompaniesHandler:
    """Handles the company-research search use case."""

    def __init__(
        self,
        discovery_port: CompanyDiscoveryPort,
        identity_port: IdentityVerificationPort,
        evidence_port: EvidenceResearchPort,
        funnel: DiscoveryFunnel | None = None,
        max_concurrent_research: int = 6,
        min_identity_confidence: str = "MEDIUM",
        budget_port: AIBudgetPort | None = None,
        ai_provider_name: str | None = None,
        directory_port: CompanyDirectoryPort | None = None,
        candidate_promoter: PromoteCandidateToCompanyHandler | None = None,
        solution_catalog: list[SolutionCatalogEntry] | None = None,
    ) -> None:
        self._discovery_port = discovery_port
        self._identity_port = identity_port
        self._evidence_port = evidence_port
        self._funnel = funnel or DiscoveryFunnel()
        self._max_concurrent_research = max(1, max_concurrent_research)
        self._min_identity_rank = _CONFIDENCE_RANK.get(min_identity_confidence.upper(), 1)
        self._budget_port = budget_port
        self._ai_provider_name = ai_provider_name
        self._directory_port = directory_port
        self._candidate_promoter = candidate_promoter
        self._solution_catalog = solution_catalog

    async def handle(self, request: CompanyResearchRequest) -> list[CompanySearchResult]:
        candidates = await self._discover_candidates(request)
        if not candidates:
            return []

        accepted, metrics = self._funnel.gate_candidates(candidates)
        logger.info(
            "Discovery funnel: discovered=%d gated_out=%d deduplicated=%d accepted=%d",
            metrics.discovered,
            metrics.deterministic_rejected,
            metrics.deduplicated,
            metrics.deterministic_accepted,
        )
        if not accepted:
            return []

        if self._budget_port is not None and self._ai_provider_name:
            # One identity-verification AI call per accepted candidate --
            # fail once, clearly, before fanning out any calls, rather than
            # partway through as N near-identical per-candidate failures.
            await self._budget_port.ensure_batch_fits(
                self._ai_provider_name, len(accepted)
            )

        semaphore = asyncio.Semaphore(self._max_concurrent_research)

        async def _research(candidate: CompanyCandidate) -> CompanySearchResult | None:
            async with semaphore:
                try:
                    return await self._research_candidate(candidate, request)
                except Exception:
                    logger.exception("Research failed for candidate %s", candidate.company_name)
                    return None

        researched = await asyncio.gather(*(_research(candidate) for candidate in accepted))

        results = [
            result
            for result in researched
            if result is not None and result.qualification_score >= request.minimum_qualification_score
        ]
        results.sort(key=lambda item: item.qualification_score, reverse=True)
        final_results = results[: request.number_of_companies]

        if request.persist_as_companies and self._candidate_promoter is not None:
            final_results = await self._promote_results(final_results)

        return final_results

    async def _promote_results(
        self, results: list[CompanySearchResult]
    ) -> list[CompanySearchResult]:
        promoted: list[CompanySearchResult] = []
        for result in results:
            try:
                company_id = await self._candidate_promoter.handle(result)
                promoted.append(result.model_copy(update={"persisted_company_id": company_id}))
            except Exception:
                logger.exception(
                    "Failed to persist Company for %s -- returning research "
                    "result without persisted_company_id",
                    result.company_name,
                )
                promoted.append(result)
        return promoted

    async def _discover_candidates(
        self, request: CompanyResearchRequest
    ) -> list[CompanyCandidate]:
        """Cheap tier first (if configured), expensive tier only to fill the
        remainder of the pool -- see docs/pamacore_aisdr_summary.md §4.
        Deduplication happens downstream in ``DiscoveryFunnel.gate_candidates``,
        so cheap- and expensive-tier results can simply be concatenated here.
        """
        if self._directory_port is None:
            return await self._discovery_port.discover(request)

        cheap = await self._directory_port.discover(request)
        if len(cheap) >= request.number_of_companies:
            logger.info(
                "Cheap-tier discovery filled the pool: %d candidates (requested %d); "
                "skipping expensive discovery",
                len(cheap),
                request.number_of_companies,
            )
            return cheap

        logger.info(
            "Cheap-tier discovery returned %d candidates (< requested %d); "
            "falling back to expensive discovery to fill the remainder",
            len(cheap),
            request.number_of_companies,
        )
        expensive = await self._discovery_port.discover(request)
        return cheap + expensive

    async def _research_candidate(
        self,
        candidate: CompanyCandidate,
        request: CompanyResearchRequest,
    ) -> CompanySearchResult | None:
        identity = await self._identity_port.verify(candidate)
        identity_rank = _CONFIDENCE_RANK.get(identity.confidence, 0)
        if identity_rank < self._min_identity_rank or identity.verified_website is None:
            return None

        evidence = await self._evidence_port.gather(candidate, identity, request)

        combined = " ".join(
            filter(None, [candidate.title, candidate.content, *(item.snippet or "" for item in evidence)])
        ).lower()

        industry = IndustryClassifier.infer_industry(combined, candidate.title, request.industries)
        industry_match, industry_reason = IndustryClassifier.matches(industry, combined, request.industries)
        if request.industries and not industry_match:
            return None

        size_match, employee_count, size_reason = IcpMatcher.matches_size(combined, request.company_size)
        if request.company_size and not size_match:
            return None

        enterprise_match, parent_from_text = IcpMatcher.enterprise_exclusion(combined, employee_count)
        if request.company_size and enterprise_match:
            return None

        signals = EvidenceSignalExtractor.extract_signals(combined)

        company_specific_evidence = [
            item for item in evidence if item.signal_scope == "company_specific"
        ]
        company_specific_text = " ".join(
            item.snippet or "" for item in company_specific_evidence
        ).lower()
        company_specific_signals = EvidenceSignalExtractor.extract_signals(company_specific_text)

        evidence_classification = EvidenceSignalExtractor.classify_evidence(
            signals,
            len(evidence),
            company_specific_signals=company_specific_signals,
            company_specific_evidence_count=len(company_specific_evidence),
        )
        scale_signal = EvidenceSignalExtractor.scale_signal(combined)

        _, recommended_services = OpportunityMapper.map_signals(signals, self._solution_catalog)
        services_matched = OpportunityMapper.any_service_matches(recommended_services, request.services)

        score = QualificationScorer.score(
            ScoringInputs(
                signals=signals,
                evidence_count=len(evidence),
                website_verified=identity.verified_website is not None,
                services_matched=services_matched,
                scale_signal=scale_signal,
            )
        )

        outcome = ResearchOutcome(
            candidate=candidate,
            identity=identity,
            evidence=evidence,
            industry=industry,
            industry_reason=industry_reason,
            employee_count=employee_count,
            icp_match=size_match,
            icp_match_reason=size_reason,
            score=score,
            evidence_classification=evidence_classification,
            signals=signals,
        )
        result = CompanyResearchMapper.to_response(outcome, request)

        if result.parent_company is None and parent_from_text:
            result = result.model_copy(update={"parent_company": parent_from_text})

        return result
