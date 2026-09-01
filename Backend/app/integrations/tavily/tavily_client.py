"""Tavily API client wrapper.

The SDK remains optional so the application and unit tests can run without
Tavily installed. Configure ``TAVILY_API_KEY`` (real environment variable
or ``.env`` file — see ``TavilySettings``) to enable live discovery.

Optionally configure ``TAVILY_API_KEY_2`` for automatic fail-over on a real
usage-limit/rate-limit error -- same mechanism and reasoning as
``GeminiClient``'s dual-key fail-over (see that module's docstring): the
retry lives entirely inside this client, so every consumer
(``TavilyDiscoveryAdapter``, ``TavilyEvidenceAdapter``, etc.) keeps working
unmodified whether one key or two are configured.
"""

from __future__ import annotations

import logging

try:
    from tavily import TavilyClient, UsageLimitExceededError
except ImportError:  # optional integration dependency
    TavilyClient = None
    UsageLimitExceededError = None

from app.infrastructure.configuration.tavily_settings import TavilySettings
from app.integrations.tavily.exceptions import TavilyRateLimitException

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

        # Optional second key -- read from settings only (no api_key_2
        # override param, mirroring GeminiClient reading its second key
        # directly off GeminiSettings rather than a generic override).
        second_key = resolved_settings.tavily_api_key_2
        self._client_2 = TavilyClient(api_key=second_key) if self._sdk_installed and second_key else None
        self._active = 1

    def search(
        self,
        query: str,
        max_results: int = 10,
        search_depth: str = "advanced",
    ) -> list[dict[str, object]]:
        """Execute a search and return normalized Tavily result records.

        If a second key is configured and the currently-active one hits a
        real usage-limit error, automatically retries once against the
        other key before giving up.
        """
        logger.info("Tavily search: %s", query)
        client = self.client if self._active == 1 else self._client_2
        if client is None:
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
            return self._search_once(client, query, max_results, search_depth)
        except TavilyRateLimitException:
            other = self._client_2 if self._active == 1 else self.client
            if other is None:
                raise
            failed_key, self._active = self._active, (2 if self._active == 1 else 1)
            logger.warning(
                "Tavily key %d rate-limited/exhausted -- failing over to key %d", failed_key, self._active
            )
            return self._search_once(other, query, max_results, search_depth)

    def _search_once(
        self,
        client: TavilyClient,
        query: str,
        max_results: int,
        search_depth: str,
    ) -> list[dict[str, object]]:
        try:
            response = client.search(
                query=query,
                search_depth=search_depth,
                max_results=max_results,
                include_answer=False,
                include_raw_content=False,
            )
            results: list[dict[str, object]] = response.get("results", [])
            logger.info("Tavily returned %d results", len(results))
            return results
        except Exception as exc:
            if UsageLimitExceededError is not None and isinstance(exc, UsageLimitExceededError):
                logger.warning("RATE_LIMIT tavily query=%r: %s", query, exc)
                raise TavilyRateLimitException(str(exc)) from exc
            logger.exception("Tavily search failed")
            return []
