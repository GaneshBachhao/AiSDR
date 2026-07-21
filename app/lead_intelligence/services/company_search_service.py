"""
Company Search Service

Builds optimized search queries and retrieves
raw company search results from the internet.
"""

from app.core.logger import logger

from app.integrations.tavily.tavily_client import (
    AgneticTavilyClient,
)

from app.lead_intelligence.schemas.lead_search_request import (
    LeadSearchRequest,
)


class CompanySearchService:
    """
    Executes company discovery searches.
    """

    def __init__(self):

        self.client = AgneticTavilyClient()

    def search(
        self,
        request: LeadSearchRequest,
    ) -> list[dict]:
        """
        Search companies using the configured
        search integration.
        """

        query = self._build_query(
            request,
        )

        logger.info("=" * 60)
        logger.info("Company Search Started")
        logger.info(f"Query : {query}")

        results = self.client.search(
            query=query,
            max_results=request.max_results,
        )

        logger.info(
            f"Search returned {len(results)} results."
        )

        logger.info("Company Search Completed")
        logger.info("=" * 60)

        return results

    def _build_query(
        self,
        request: LeadSearchRequest,
    ) -> str:
        """
        Build an optimized internet search query.
        """

        parts = [

            f"{request.industry} companies",

            f"in {request.location}",

            "official website",

        ]

        if request.keywords:

            parts.extend(
                request.keywords,
            )

        return " ".join(parts)