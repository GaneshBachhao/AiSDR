"""
Application port for discovering public-web contacts at a qualified
company candidate.

This is the fourth external boundary in the research pipeline (discover ->
verify identity -> gather evidence -> discover contacts). Like
``EvidenceResearchPort``, it only runs for candidates that have already
cleared everything upstream -- in this case, qualification scoring as well,
per docs/product_backlog.md EPIC-05 story 5.2 ("Adapter never invoked below
minimum_qualification_score").
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.application.company_research.dto.company_research_response import (
    DiscoveredContact,
)
from app.domain.company_research.entities.candidate import CompanyCandidate


class ContactDiscoveryPort(ABC):
    """Application port for discovering decision-maker contacts at a company."""

    @abstractmethod
    async def discover(
        self,
        candidate: CompanyCandidate,
        website: str | None,
        target_role: str | None,
    ) -> list[DiscoveredContact]:
        """Return public-web-sourced contacts, best-effort.

        ``target_role`` (when provided) should steer the search toward that
        role -- e.g. a "COO / Operations Leader" catalog match should search
        for operations leadership, not a generic contact. Must never
        fabricate a contact: no matching public profile means an empty list,
        not a guess.
        """
        raise NotImplementedError
