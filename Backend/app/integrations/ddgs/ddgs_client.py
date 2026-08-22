"""ddgs (DuckDuckGo) search client wrapper.

Free, keyless alternative to Tavily -- selected via ``SEARCH_PROVIDER=ddgs``
(see ``SearchProviderSettings``). Deliberately structurally interchangeable
with ``AgneticTavilyClient`` (same ``search()`` signature and Tavily-shaped
``{title, url, content}`` return records) so every existing consumer
(``TavilyDiscoveryAdapter``, ``TavilyEvidenceAdapter``,
``TavilyContactDiscoveryAdapter``, ``TavilyDirectoryAdapter``,
``AiIdentityVerificationAdapter``) works unchanged when the flag flips.

The SDK remains optional so the application and unit tests can run without
``ddgs`` installed, mirroring ``app/integrations/tavily/tavily_client.py``.
"""

from __future__ import annotations

import logging
from urllib.parse import urlparse

try:
    from ddgs import DDGS
    from ddgs.exceptions import RatelimitException
except ImportError:  # optional integration dependency
    DDGS = None
    RatelimitException = None

from app.integrations.tavily.exceptions import TavilyRateLimitException

logger = logging.getLogger(__name__)

# ddgs-only noise reduction (never applied to Tavily results -- Tavily's own
# results pass through TavilyDiscoveryAdapter's existing blocked-domain/
# title-marker gate unchanged). Real, live discovery-only comparisons (zero
# AI cost -- discovery has no LLM call) against "Manufacturing companies in
# {geography}"-style queries showed ddgs's plain-search ranking surfaces
# noticeably more government/association/directory/HR-publication/staffing-
# agency/news pages than Tavily's curated results do for the same query
# text, and the shared adapter's own title-marker check is startswith-
# anchored (tuned against Tavily's typical phrasing), so it missed titles
# like "Manufacturing Hiring Trends 2026: Skills, Jobs, Key Challenges" or
# "American Companies Directory -- Search 8,000+ US Companies" where the
# noise word isn't the first word. This is a substring check specifically
# to catch that.
#
# Confirmed by two real (free, zero-AI) recruiting/media candidates that
# reached identity verification before this list covered the general root
# words: a staffing consultancy whose own domain literally contained
# "placements" (only the narrower "placement consultants"/"recruitment
# agency" phrases were blocked at the time, not the bare root word), and a
# major newspaper portal (a keyword can't safely catch every news outlet by
# name -- "times"/"news" alone false-positive on real companies like "Times
# Microwave Systems" -- so well-known news-portal domains are blocked by
# domain instead, the same curated-blocklist approach
# DeterministicCandidateGate already uses for known-junk Tavily-side
# domains like justdial.com/indiamart.com). Add more here as encountered
# rather than trying to be exhaustive up front.
_QUERY_NOISE_EXCLUSIONS = (
    ' -jobs -careers -recruitment -staffing -placements -directory -"chamber of commerce"'
)

_NOISE_TITLE_SUBSTRINGS = (
    "directory",
    "database",
    "hiring trends",
    "job openings",
    "recruitment",
    "staffing",
    "placement",
    "chamber of commerce",
    "newspaper",
    "magazine",
    "association of manufacturers",
)

_NOISE_DOMAIN_SUFFIXES = (".gov", ".gov.in")

# Search-engine redirect artifacts, plus a small, non-exhaustive starter set
# of well-known news/media portals observed as false positives in testing.
_NOISE_DOMAINS = frozenset(
    {
        "bing.com",
        "google.com",
        "duckduckgo.com",
        "indiatimes.com",
        "ndtv.com",
        "hindustantimes.com",
        "thehindu.com",
    }
)


class DdgsClient:
    """Small boundary around the optional ``ddgs`` SDK.

    Reuses ``TavilyRateLimitException`` for a ddgs rate-limit signal rather
    than introducing a second, provider-specific exception type -- every
    existing caller that catches ``TavilyRateLimitException`` to propagate a
    "this candidate was never actually checked" signal distinctly (see
    ``AiIdentityVerificationAdapter.verify()``, ``SearchCompaniesHandler``)
    needs that behavior regardless of which search provider is active, and
    duplicating the exception type per provider would make callers need to
    catch both. The name is a pre-existing minor inaccuracy once a second
    provider raises it, not a new one this file introduces.
    """

    def __init__(self) -> None:
        self._sdk_installed = DDGS is not None

    def search(
        self,
        query: str,
        max_results: int = 10,
        search_depth: str = "advanced",
    ) -> list[dict[str, object]]:
        """Execute a search and return Tavily-shaped result records.

        ``search_depth`` is accepted for interface parity with
        ``AgneticTavilyClient.search()`` but has no ddgs equivalent, so it's
        ignored.
        """
        logger.info("ddgs search: %s", query)
        if not self._sdk_installed:
            logger.warning(
                "ddgs is unavailable: the 'ddgs' package is not installed. "
                "Run 'pip install ddgs' to enable it as a search provider."
            )
            return []

        try:
            raw_results = DDGS().text(query + _QUERY_NOISE_EXCLUSIONS, max_results=max_results)
            results = [
                {
                    "title": item.get("title", ""),
                    "url": item.get("href", ""),
                    "content": item.get("body", ""),
                }
                for item in raw_results
                if not self._is_noise(item.get("title", ""), item.get("href", ""))
            ]
            logger.info("ddgs returned %d results (noise filtered)", len(results))
            return results
        except Exception as exc:
            if RatelimitException is not None and isinstance(exc, RatelimitException):
                logger.warning("RATE_LIMIT ddgs query=%r: %s", query, exc)
                raise TavilyRateLimitException(str(exc)) from exc
            logger.exception("ddgs search failed")
            return []

    @staticmethod
    def _is_noise(title: str, url: str) -> bool:
        """True if this result is a category that's never a genuine company
        lead (government/association/directory/HR-publication/staffing-
        agency/news page), per the ddgs-specific noise patterns documented
        above the module constants.
        """
        normalized_title = title.strip().casefold()
        if any(marker in normalized_title for marker in _NOISE_TITLE_SUBSTRINGS):
            return True

        domain = urlparse(url).netloc.casefold().removeprefix("www.")
        if not domain:
            return False
        # A staffing/recruitment agency's own domain very often spells its
        # business out directly (e.g. "shriniwasplacements.com") even when
        # the page title doesn't -- check the domain against the same root
        # words, not just known-junk exact domains.
        if any(marker in domain for marker in _NOISE_TITLE_SUBSTRINGS):
            return True
        if any(domain == item or domain.endswith("." + item) for item in _NOISE_DOMAINS):
            return True
        return any(domain.endswith(suffix) for suffix in _NOISE_DOMAIN_SUFFIXES)
