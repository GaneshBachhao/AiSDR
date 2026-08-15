"""
Application port for the cheap-tier ("Company Universe") discovery stage.

Distinct from ``CompanyDiscoveryPort`` on purpose, even though the method
signature is identical: this port represents a different cost/SLA
contract -- structured, high-candidates-per-call sources (directories,
registries) that should always be tried *before* the broader, more
expensive web-search discovery. See docs/pamacore_aisdr_summary.md §4's
asymmetric funnel and Track 1 Phase 2.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.application.company_research.dto.company_research_request import (
    CompanyResearchRequest,
)
from app.domain.company_research.entities.candidate import CompanyCandidate


class CompanyDirectoryPort(ABC):
    """Application port for the cheap, structured-source discovery tier."""

    @abstractmethod
    async def discover(
        self,
        request: CompanyResearchRequest,
    ) -> list[CompanyCandidate]:
        """Return candidate companies from cheap, structured sources only.

        Implementations should prioritize sources that return many
        candidates per query (directory/listing pages, registries) over
        one-candidate-per-query web search -- that's what keeps this tier
        cheap relative to ``CompanyDiscoveryPort``. Returning an empty or
        partial list is expected and normal; callers fall back to the
        broader discovery port to fill the remainder of the candidate pool.
        """
        raise NotImplementedError
