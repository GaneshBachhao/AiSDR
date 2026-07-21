"""
Tavily Client

Encapsulates all interaction with the Tavily API.
"""

from tavily import TavilyClient

from app.core.config import settings
from app.core.logger import logger


class AgneticTavilyClient:
    """
    Wrapper around the Tavily SDK.
    """

    def __init__(self):

        self.client = TavilyClient(
            api_key=settings.TAVILY_API_KEY
        )

    def search(
        self,
        query: str,
        max_results: int = 10,
    ) -> list[dict]:
        """
        Execute a web search.

        Returns only the search results list.
        """

        logger.info(
            f"Tavily Search : {query}"
        )

        try:

            response = self.client.search(
                query=query,
                search_depth="advanced",
                max_results=max_results,
                include_answer=False,
                include_raw_content=False,
            )

            results = response.get(
                "results",
                [],
            )

            logger.info(
                f"Tavily returned {len(results)} results."
            )

            return results

        except Exception as ex:

            logger.exception(
                f"Tavily Search Failed : {str(ex)}"
            )

            return []