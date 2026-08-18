"""
Tavily-backed implementation of ``CompanyDiscoveryPort``.

Builds a candidate pool of real companies from public-web search results.
A directory/listing page is never itself returned as a company candidate;
its title/URL/record-count is retained as ``discovery_metadata`` on any
company names it happens to list, and its own row-extraction is treated as
one more discovery source. No identity verification, industry
classification, or deep research happens here -- this port answers only
"which companies might be relevant", per its contract.
"""

from __future__ import annotations

import asyncio
import logging
import re
from datetime import UTC, datetime
from urllib.parse import urlparse

from app.application.company_research.dto.company_research_request import (
    CompanyResearchRequest,
)
from app.application.company_research.ports.company_discovery_port import (
    CompanyDiscoveryPort,
)
from app.domain.company_research.entities.candidate import CompanyCandidate
from app.domain.company_research.services.candidate_gate import DeterministicCandidateGate
from app.infrastructure.configuration.company_research_settings import (
    CompanyResearchSettings,
)
from app.integrations.tavily.exceptions import TavilyRateLimitException
from app.integrations.tavily.tavily_client import AgneticTavilyClient

logger = logging.getLogger(__name__)

_GENERIC_TITLE_MARKERS = (
    "top ",
    "best ",
    "list of",
    "companies in",
    "companies using",
    "companies that",
    "directory",
    "market report",
    "industry report",
    "press release",
    "news",
    "blog",
    "case study",
    "guide",
    "how to",
    "jobs",
    "job openings",
    "hiring",
    "events",
)

_DISCOVERY_TITLE_MARKERS = (
    "companies in",
    "companies —",
    "companies -",
    "records",
    "business directory",
    "company directory",
    "company database",
    "manufacturing database",
)


class TavilyDiscoveryAdapter(CompanyDiscoveryPort):
    """Discovers company candidates from Tavily public-web search."""

    def __init__(
        self,
        client: AgneticTavilyClient | None = None,
        settings: CompanyResearchSettings | None = None,
    ) -> None:
        self._client = client or AgneticTavilyClient()
        self._settings = settings or CompanyResearchSettings()

    async def discover(self, request: CompanyResearchRequest) -> list[CompanyCandidate]:
        raw_candidates = await asyncio.to_thread(self._discover_candidates, request)
        return [self._to_domain_candidate(item) for item in raw_candidates]

    # -- discovery ---------------------------------------------------------

    def _discover_candidates(self, request: CompanyResearchRequest) -> list[dict]:
        industries = request.industries or ["companies"]
        queries: list[str] = []

        for industry in industries:
            base = f"{industry} companies in {request.geography} official company website"
            if request.company_size:
                base += " " + " ".join(request.company_size[:3])
            queries.extend(
                [
                    base,
                    f"{industry} manufacturers companies {request.geography} official website"
                    if industry.lower() == "manufacturing"
                    else f"{industry} companies {request.geography} products services official website",
                    f"{industry} companies {request.geography} expansion hiring technology",
                    f"{industry} companies {request.geography} directory database records",
                ]
            )

        candidates: list[dict] = []
        seen_domains: set[str] = set()
        seen_names: set[str] = set()
        target_pool = min(
            max(
                request.number_of_companies * self._settings.candidate_pool_multiplier,
                self._settings.candidate_pool_min,
            ),
            self._settings.candidate_pool_max,
        )

        for query in queries:
            try:
                query_results = self._client.search(
                    query=query,
                    max_results=min(target_pool, 30),
                    search_depth="basic",
                )
            except TavilyRateLimitException as exc:
                # Non-fatal: this query's candidates are simply missing
                # from the pool, same as if it had genuinely returned zero
                # results -- but logged clearly (unlike before this
                # exception existed) so a rate-limited discovery pass that
                # ends up returning few/no candidates is distinguishable
                # from "there really are no matching companies."
                logger.warning("RATE_LIMIT tavily discovery query=%r: %s", query, exc)
                continue
            for item in query_results:
                url = str(item.get("url", "")).strip()
                title = str(item.get("title", "")).strip()
                content = str(item.get("content", "")).strip()
                if not url or not title:
                    continue

                domain = urlparse(url).netloc.lower().removeprefix("www.")
                if not domain or self._blocked_domain(domain):
                    continue

                discovery = self._discovery_metadata(title, url, content)
                if discovery:
                    for extracted in self._extract_directory_candidates(content, request.geography):
                        self._append_candidate(candidates, seen_names, seen_domains, extracted, discovery)
                    continue

                if self._looks_like_article_title(title) or domain in seen_domains:
                    continue

                name = self._candidate_name(title, domain)
                if self._invalid_candidate_name(name):
                    continue
                normalized_name = self._normalize_name(name)
                if normalized_name in seen_names:
                    continue

                seen_names.add(normalized_name)
                seen_domains.add(domain)
                candidates.append(
                    {
                        "company_name": name,
                        "website": self._root_url(url),
                        "title": title,
                        "content": content,
                        "url": url,
                        "discovery_metadata": [],
                    }
                )

                if len(candidates) >= target_pool:
                    return candidates

        return candidates

    @classmethod
    def _append_candidate(
        cls,
        candidates: list[dict],
        seen_names: set[str],
        seen_domains: set[str],
        candidate: dict,
        source_metadata: dict,
    ) -> None:
        name = str(candidate.get("company_name", "")).strip()
        if not name or cls._invalid_candidate_name(name):
            return
        normalized_name = cls._normalize_name(name)
        if normalized_name in seen_names:
            for existing in candidates:
                if cls._normalize_name(existing.get("company_name", "")) == normalized_name:
                    metadata = existing.setdefault("discovery_metadata", [])
                    if source_metadata not in metadata:
                        metadata.append(source_metadata)
                    return
            return

        domain = urlparse(str(candidate.get("website", ""))).netloc.lower().removeprefix("www.")
        if domain and domain in seen_domains:
            return

        seen_names.add(normalized_name)
        if domain:
            seen_domains.add(domain)
        candidate["discovery_metadata"] = [source_metadata]
        candidates.append(candidate)

    @classmethod
    def _discovery_metadata(cls, title: str, url: str, content: str) -> dict | None:
        normalized = " ".join(title.lower().split())
        count = cls._extract_record_count(f"{title} {content}")
        is_discovery_title = any(marker in normalized for marker in _DISCOVERY_TITLE_MARKERS)
        has_many_company_rows = bool(cls._extract_directory_candidates(content, None))
        if not is_discovery_title and not count and not has_many_company_rows:
            return None
        return {
            "source_type": "discovery_directory",
            "source_title": title,
            "source_url": url,
            "discovered_record_count": count,
            "metadata_observed_at": datetime.now(UTC).isoformat(),
        }

    @staticmethod
    def _extract_record_count(text: str) -> int | None:
        patterns = (
            r"\b([0-9]{1,3}(?:,[0-9]{3})+|[0-9]+)\s+records?\b",
            r"\b([0-9]+(?:\.[0-9]+)?)\s*(million|m)\+?\s+(?:companies|records)\b",
        )
        for index, pattern in enumerate(patterns):
            match = re.search(pattern, text, flags=re.IGNORECASE)
            if not match:
                continue
            if index == 0:
                return int(match.group(1).replace(",", ""))
            return int(float(match.group(1)) * 1_000_000)
        return None

    @classmethod
    def _extract_directory_candidates(cls, content: str, geography: str | None) -> list[dict]:
        if not content:
            return []
        lines = [line.strip(" -*|:") for line in content.splitlines() if line.strip()]
        candidates: list[dict] = []
        for index, line in enumerate(lines):
            if line.lower() != "country":
                continue
            if index == 0:
                continue
            name = lines[index - 1].strip()
            if not cls._looks_like_company_name(name):
                continue
            location_parts: list[str] = []
            for following in lines[index + 1 : index + 5]:
                if following.lower() in {"sales revenue ($m)", "sales revenue", "revenue"}:
                    break
                if following.lower() == "country":
                    break
                location_parts.append(following)
                if following.lower() in {"india", "usa", "us", "united states", "uk", "canada"}:
                    break
            location = ", ".join(location_parts).strip(" ,")
            if geography and geography.lower() not in location.lower():
                continue
            candidates.append(
                {
                    "company_name": name,
                    "website": None,
                    "title": name,
                    "content": f"{name}\nCountry: {location}",
                    "url": "",
                }
            )
        return candidates

    @staticmethod
    def _looks_like_company_name(value: str) -> bool:
        value = " ".join(value.split())
        if len(value) < 3 or len(value) > 120:
            return False
        lowered = value.lower()
        if lowered in {"country", "sales revenue ($m)", "sales revenue", "company", "companies"}:
            return False
        if any(
            marker in lowered
            for marker in (
                "find manufacturing",
                "manufacturing companies",
                "company database",
                "company directory",
                "records",
                "search results",
                "page ",
            )
        ):
            return False
        return sum(char.isalpha() for char in value) >= 3

    @classmethod
    def _invalid_candidate_name(cls, name: str) -> bool:
        normalized = " ".join(name.lower().split())
        return (
            not cls._looks_like_company_name(name)
            or cls._looks_like_article_title(name)
            or normalized.startswith(("find ", "top ", "best ", "list of "))
        )

    @staticmethod
    def _normalize_name(name: str) -> str:
        return re.sub(r"[^a-z0-9]+", " ", name.lower()).strip()

    @classmethod
    def _looks_like_article_title(cls, title: str) -> bool:
        normalized = " ".join(title.lower().split())
        if any(normalized.startswith(marker) for marker in _GENERIC_TITLE_MARKERS):
            return True
        if len(normalized) > 110 and any(
            token in normalized for token in ("companies", "manufacturing", "digital transformation")
        ):
            return True
        return False

    @classmethod
    def _candidate_name(cls, title: str, domain: str) -> str:
        host = domain.split(".")[0].replace("-", " ").strip()
        cleaned = title.strip()
        if " | " in cleaned:
            cleaned = cleaned.split(" | ", 1)[0].strip()
        if " - " in cleaned:
            cleaned = cleaned.split(" - ", 1)[0].strip()
        lowered = f" {cleaned.lower()} "
        action_title = any(
            marker in lowered
            for marker in (
                " collaborates ",
                " announces ",
                " partners with ",
                " selects ",
                " launches ",
                " unveils ",
                " acquires ",
                " joins ",
                " to deliver ",
            )
        )
        if not cleaned or len(cleaned.split()) > 8 or action_title or cls._looks_like_article_title(cleaned):
            cleaned = host.title()
        return cleaned

    @staticmethod
    def _blocked_domain(domain: str) -> bool:
        domain = domain.lower().removeprefix("www.")
        blocked = DeterministicCandidateGate.DEFAULT_BLOCKED_DOMAINS
        return any(domain == item or domain.endswith("." + item) for item in blocked)

    @staticmethod
    def _root_url(url: str) -> str:
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"

    @staticmethod
    def _to_domain_candidate(raw: dict) -> CompanyCandidate:
        metadata = raw.get("discovery_metadata") or []
        source_url = raw.get("url") or (metadata[0].get("source_url") if metadata else "")
        return CompanyCandidate(
            company_name=str(raw.get("company_name", "")).strip(),
            website=raw.get("website"),
            title=str(raw.get("title", "")).strip(),
            content=str(raw.get("content", "")),
            source_url=str(source_url or ""),
            discovery_metadata=metadata,
        )
