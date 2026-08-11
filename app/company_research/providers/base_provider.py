from __future__ import annotations

from abc import ABC, abstractmethod

from app.company_research.schemas.company_research import (
    CompanyResearchRequest,
    CompanySearchResult,
)


class CompanyResearchProvider(ABC):
    """Provider contract for public-web company discovery and research."""

    @abstractmethod
    def discover(
        self,
        request: CompanyResearchRequest,
    ) -> list[CompanySearchResult]:
        """Discover and research companies from permitted public sources."""
        raise NotImplementedError
