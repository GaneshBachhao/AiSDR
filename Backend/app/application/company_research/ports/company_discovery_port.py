"""
Application port for sourcing company candidates.

This abstraction decouples the application layer from any specific
discovery mechanism (Tavily web search today; Company Universe or
directory ingestion later). Implementations live in the infrastructure
layer as adapters and must return Domain entities only.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.application.company_research.dto.company_research_request import (
    CompanyResearchRequest,
)
from app.domain.company_research.entities.candidate import CompanyCandidate


class CompanyDiscoveryPort(ABC):
    """Application port for discovering company candidates from an external source."""

    @abstractmethod
    async def discover(
        self,
        request: CompanyResearchRequest,
    ) -> list[CompanyCandidate]:
        """Return candidate companies for the given request.

        Implementations must not perform identity verification or research
        here — this port answers "which companies might be relevant", not
        "is this actually that company" or "what evidence exists about it".
        """
        raise NotImplementedError
