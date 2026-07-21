"""
Search Provider

Discovers companies using internet search and converts
raw search results into normalized LeadCandidate objects.
"""

from urllib.parse import urlparse

from app.core.logger import logger

from app.discovery.providers.base_provider import BaseDiscoveryProvider

from app.lead_intelligence.schemas.lead_candidate_schema import (
    LeadCandidate,
)

from app.lead_intelligence.schemas.lead_search_request import (
    LeadSearchRequest,
)

from app.lead_intelligence.services.company_search_service import (
    CompanySearchService,
)


class SearchProvider(BaseDiscoveryProvider):
    """
    Internet search-based discovery provider.
    """

    def __init__(self):

        self.search_service = CompanySearchService()

    def discover(
        self,
        industry: str,
        location: str,
        max_results: int,
    ) -> list[LeadCandidate]:
        """
        Discover companies from internet search.
        """

        request = LeadSearchRequest(
            industry=industry,
            location=location,
            max_results=max_results,
        )

        raw_results = self.search_service.search(
            request=request,
        )

        candidates = []

        for result in raw_results:

            if not self._is_valid_result(result):
                continue

            candidate = self._to_candidate(result)

            if candidate:

                candidates.append(candidate)

        logger.info(
            f"Valid candidates discovered: {len(candidates)}"
        )

        return candidates

    def _is_valid_result(
        self,
        result: dict,
    ) -> bool:
        """
        Validate whether a search result
        looks like a company website.
        """

        title = (
            result.get("title", "")
            .strip()
        )

        url = (
            result.get("url", "")
            .strip()
            .lower()
        )

        if not title:
            return False

        if not url:
            return False

        blocked_domains = [

            "wikipedia.org",

            "facebook.com",

            "linkedin.com",

            "youtube.com",

            "twitter.com",

            "x.com",

            "instagram.com",

            "indiamart.com",

            "tradeindia.com",

            "justdial.com",

            "sulekha.com",
        ]

        blocked_extensions = [

            ".pdf",

            ".doc",

            ".docx",

            ".ppt",

            ".pptx",

            ".xls",

            ".xlsx",

            ".zip",

            ".rar",
        ]

        blocked_keywords = [

            "pdf",

            "document",

            "download",

            "report",

            "whitepaper",

            "brochure",

            "manual",

            "blog",

            "news",

            "article",

            "top 10",

            "top 20",

            "list of",

            "directory",
        ]

        for domain in blocked_domains:

            if domain in url:

                return False

        for extension in blocked_extensions:

            if url.endswith(extension):

                return False

        title_lower = title.lower()

        for keyword in blocked_keywords:

            if keyword in title_lower:

                return False

        return True

    def _to_candidate(
        self,
        result: dict,
    ) -> LeadCandidate | None:
        """
        Convert Tavily result into LeadCandidate.
        """

        url = result.get(
            "url",
        )

        if not url:

            return None

        parsed = urlparse(url)

        company_name = result.get(
            "title",
            parsed.netloc,
        )

        return LeadCandidate(

            company_name=company_name,

            website=url,

            source="tavily",

            confidence=float(
                result.get(
                    "score",
                    0.8,
                )
            ),

            metadata={

                "title": result.get(
                    "title",
                ),

                "content": result.get(
                    "content",
                ),

                "url": url,
            },
        )