"""
Tavily-backed implementation of ``EvidenceResearchPort``.

Only runs for candidates that have already passed identity verification.
Gathers public-web evidence of buying signals (technology hiring, growth,
funding, requested-service-specific activity) for the verified company.
"""

from __future__ import annotations

import asyncio
from urllib.parse import urlparse

from app.application.company_research.dto.company_research_request import (
    CompanyResearchRequest,
)
from app.application.company_research.dto.company_research_response import EvidenceItem
from app.application.company_research.ports.evidence_research_port import (
    EvidenceResearchPort,
)
from app.application.company_research.ports.identity_verification_port import (
    IdentityVerificationResult,
)
from app.domain.company_research.entities.candidate import CompanyCandidate
from app.domain.company_research.services.candidate_gate import DeterministicCandidateGate
from app.infrastructure.configuration.company_research_settings import (
    CompanyResearchSettings,
)
from app.integrations.tavily.tavily_client import AgneticTavilyClient


class TavilyEvidenceAdapter(EvidenceResearchPort):
    """Gathers buying-signal evidence for a verified company via Tavily."""

    def __init__(
        self,
        client: AgneticTavilyClient | None = None,
        settings: CompanyResearchSettings | None = None,
    ) -> None:
        self._client = client or AgneticTavilyClient()
        self._settings = settings or CompanyResearchSettings()

    async def gather(
        self,
        candidate: CompanyCandidate,
        identity: IdentityVerificationResult,
        request: CompanyResearchRequest,
    ) -> list[EvidenceItem]:
        return await asyncio.to_thread(self._gather, candidate, request)

    def _gather(
        self,
        candidate: CompanyCandidate,
        request: CompanyResearchRequest,
    ) -> list[EvidenceItem]:
        name = candidate.company_name
        period = request.research_period.strip() if request.research_period else "recent"
        max_items = self._settings.max_evidence_items

        queries = [
            f'"{name}" technology AI automation cloud hiring expansion {period}',
            f'"{name}" funding acquisition new product transformation modernization {period}',
        ]
        if request.services:
            queries.append(f'"{name}" ' + " ".join(request.services[:4]) + f" {period}")

        evidence: list[EvidenceItem] = []
        seen_urls: set[str] = set()

        for query in queries:
            for item in self._client.search(query=query, max_results=5, search_depth="advanced"):
                url = str(item.get("url", "")).strip()
                title = str(item.get("title", "")).strip()
                snippet = str(item.get("content", "")).strip()
                if not url or not title or url in seen_urls:
                    continue
                if self._blocked_domain(urlparse(url).netloc.lower()):
                    continue
                seen_urls.add(url)
                evidence.append(
                    EvidenceItem(
                        title=title,
                        url=url,
                        snippet=snippet[:800] if snippet else None,
                        evidence_date=(
                            str(item.get("published_date") or item.get("date") or "").strip() or None
                        ),
                    )
                )
                if len(evidence) >= max_items:
                    return evidence
            if len(evidence) >= max_items:
                break

        return evidence

    @staticmethod
    def _blocked_domain(domain: str) -> bool:
        domain = domain.lower().removeprefix("www.")
        blocked = DeterministicCandidateGate.DEFAULT_BLOCKED_DOMAINS
        return any(domain == item or domain.endswith("." + item) for item in blocked)
