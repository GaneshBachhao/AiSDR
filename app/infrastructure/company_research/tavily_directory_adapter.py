"""
Tavily-backed implementation of ``CompanyDirectoryPort`` -- the cheap
discovery tier.

Unlike ``TavilyDiscoveryAdapter`` (one candidate per search result), this
adapter only harvests structured directory/listing pages, where a single
Tavily query can yield dozens of candidates at once. It deliberately does
*not* fall back to single-company search results -- that's what makes it
"cheap" relative to the broader adapter, and why ``SearchCompaniesHandler``
tries this tier first and only calls the expensive one to fill the
remainder of the candidate pool.

Results are cached in-memory per (industries, geography, company_size),
so repeated requests for the same sector/region within
``CompanyResearchSettings.directory_cache_ttl_seconds`` don't re-query
Tavily at all.

Directory-row parsing is intentionally reused from ``TavilyDiscoveryAdapter``
rather than duplicated -- see its ``_discovery_metadata``/
``_extract_directory_candidates``/``_to_domain_candidate`` classmethods.
"""

from __future__ import annotations

import asyncio
import time
from urllib.parse import urlparse

from app.application.company_research.dto.company_research_request import (
    CompanyResearchRequest,
)
from app.application.company_research.ports.company_directory_port import (
    CompanyDirectoryPort,
)
from app.domain.company_research.entities.candidate import CompanyCandidate
from app.infrastructure.company_research.tavily_discovery_adapter import (
    TavilyDiscoveryAdapter,
)
from app.infrastructure.configuration.company_research_settings import (
    CompanyResearchSettings,
)
from app.integrations.tavily.tavily_client import AgneticTavilyClient

CacheKey = tuple[tuple[str, ...], str, tuple[str, ...]]


class TavilyDirectoryAdapter(CompanyDirectoryPort):
    """Cheap-tier discovery: mines structured directory pages, with caching."""

    def __init__(
        self,
        client: AgneticTavilyClient | None = None,
        settings: CompanyResearchSettings | None = None,
    ) -> None:
        self._client = client or AgneticTavilyClient()
        self._settings = settings or CompanyResearchSettings()
        self._cache: dict[CacheKey, tuple[float, list[CompanyCandidate]]] = {}

    async def discover(self, request: CompanyResearchRequest) -> list[CompanyCandidate]:
        cache_key = self._cache_key(request)
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached

        raw_candidates = await asyncio.to_thread(self._discover_candidates, request)
        candidates = [TavilyDiscoveryAdapter._to_domain_candidate(item) for item in raw_candidates]
        self._cache[cache_key] = (time.monotonic(), candidates)
        return candidates

    # -- caching -------------------------------------------------------

    @staticmethod
    def _cache_key(request: CompanyResearchRequest) -> CacheKey:
        return (
            tuple(sorted(i.strip().lower() for i in request.industries)),
            request.geography.strip().lower(),
            tuple(sorted(s.strip().lower() for s in request.company_size)),
        )

    def _get_cached(self, key: CacheKey) -> list[CompanyCandidate] | None:
        entry = self._cache.get(key)
        if entry is None:
            return None
        cached_at, candidates = entry
        if time.monotonic() - cached_at > self._settings.directory_cache_ttl_seconds:
            del self._cache[key]
            return None
        return candidates

    # -- discovery -------------------------------------------------------

    def _discover_candidates(self, request: CompanyResearchRequest) -> list[dict]:
        industries = request.industries or ["companies"]
        target_pool = min(
            max(
                request.number_of_companies * self._settings.candidate_pool_multiplier,
                self._settings.candidate_pool_min,
            ),
            self._settings.candidate_pool_max,
        )

        candidates: list[dict] = []
        seen_names: set[str] = set()
        seen_domains: set[str] = set()

        for industry in industries:
            queries = [
                f"{industry} companies directory database {request.geography}",
                f"{industry} companies list {request.geography} records",
            ]
            for query in queries:
                for item in self._client.search(query=query, max_results=10, search_depth="basic"):
                    url = str(item.get("url", "")).strip()
                    title = str(item.get("title", "")).strip()
                    content = str(item.get("content", "")).strip()
                    if not title or not content:
                        continue

                    domain = urlparse(url).netloc.lower().removeprefix("www.") if url else ""
                    if domain and TavilyDiscoveryAdapter._blocked_domain(domain):
                        continue

                    discovery = TavilyDiscoveryAdapter._discovery_metadata(title, url, content)
                    if not discovery:
                        # Not a directory/listing page -- skip. Treating a
                        # single search result as one candidate is the
                        # expensive tier's job, not this one's.
                        continue

                    extracted = TavilyDiscoveryAdapter._extract_directory_candidates(
                        content, request.geography
                    )
                    for candidate in extracted:
                        TavilyDiscoveryAdapter._append_candidate(
                            candidates, seen_names, seen_domains, candidate, discovery
                        )
                        if len(candidates) >= target_pool:
                            return candidates

        return candidates
