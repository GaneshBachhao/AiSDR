from __future__ import annotations

from app.company_research.providers.base_provider import CompanyResearchProvider
from app.company_research.schemas.company_research import (
    CompanyResearchRequest,
    CompanySearchResult,
)


class CompanyResearchService:
    """Application service for Step 1 public-web company research."""

    def __init__(self, provider: CompanyResearchProvider | None = None) -> None:
        if provider is None:
            from app.company_research.providers.tavily_provider import (
                TavilyCompanyResearchProvider,
            )
            provider = TavilyCompanyResearchProvider()
        self._provider = provider

    def search(
        self,
        request: CompanyResearchRequest,
    ) -> list[CompanySearchResult]:
        return self._provider.discover(request)
