"""Tavily API client wrapper.

The SDK remains optional so the application and unit tests can run without
Tavily installed. Configure ``TAVILY_API_KEY`` to enable live discovery.
"""

from __future__ import annotations

import logging
import os

try:
    from tavily import TavilyClient
except ImportError:  # optional integration dependency
    TavilyClient = None

logger = logging.getLogger(__name__)


class AgneticTavilyClient:
    """Small boundary around the optional Tavily SDK."""

    def __init__(self, api_key: str | None = None) -> None:
        key = api_key or os.getenv("TAVILY_API_KEY", "")
        self.client = TavilyClient(api_key=key) if TavilyClient and key else None

    def search(
        self,
        query: str,
        max_results: int = 10,
        search_depth: str = "advanced",
    ) -> list[dict]:
        """Execute a search and return normalized Tavily result records."""
        logger.info("Tavily search: %s", query)
        if self.client is None:
            logger.warning(
                "Tavily is unavailable; install tavily-python and set TAVILY_API_KEY "
                "for live company discovery."
            )
            return []

        try:
            response = self.client.search(
                query=query,
                search_depth=search_depth,
                max_results=max_results,
                include_answer=False,
                include_raw_content=False,
            )
            results = response.get("results", [])
            logger.info("Tavily returned %d results", len(results))
            return results
        except Exception:
            logger.exception("Tavily search failed")
            return []
