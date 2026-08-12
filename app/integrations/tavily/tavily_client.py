"""Tavily API client wrapper.

The SDK remains optional so the application and unit tests can run without
Tavily installed. Configure ``TAVILY_API_KEY`` (real environment variable
or ``.env`` file — see ``TavilySettings``) to enable live discovery.
"""

from __future__ import annotations

import logging

try:
    from tavily import TavilyClient
except ImportError:  # optional integration dependency
    TavilyClient = None

from app.infrastructure.configuration.tavily_settings import TavilySettings

logger = logging.getLogger(__name__)


class AgneticTavilyClient:
    """Small boundary around the optional Tavily SDK."""

    def __init__(
        self,
        api_key: str | None = None,
        settings: TavilySettings | None = None,
    ) -> None:
        resolved_settings = settings or TavilySettings()
        key = api_key or resolved_settings.tavily_api_key
        self._sdk_installed = TavilyClient is not None
        self._key_configured = bool(key)
        self.client = TavilyClient(api_key=key) if self._sdk_installed and self._key_configured else None

    def search(
        self,
        query: str,
        max_results: int = 10,
        search_depth: str = "advanced",
    ) -> list[dict[str, object]]:
        """Execute a search and return normalized Tavily result records."""
        logger.info("Tavily search: %s", query)
        if self.client is None:
            if not self._sdk_installed:
                logger.warning(
                    "Tavily is unavailable: the 'tavily-python' package is not installed. "
                    "Run 'pip install tavily-python' to enable live company discovery."
                )
            elif not self._key_configured:
                logger.warning(
                    "Tavily is unavailable: TAVILY_API_KEY is not set. Export it as a real "
                    "environment variable, or add TAVILY_API_KEY=... to a local .env file, "
                    "to enable live company discovery."
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
            results: list[dict[str, object]] = response.get("results", [])
            logger.info("Tavily returned %d results", len(results))
            return results
        except Exception:
            logger.exception("Tavily search failed")
            return []
