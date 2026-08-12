from __future__ import annotations

from dataclasses import dataclass, field
from urllib.parse import urlparse


@dataclass(slots=True)
class CompanyCandidate:
    """Cheap, normalized company candidate used before paid identity verification and research.

    This entity is intentionally minimal and network-free: it represents a
    single search-result-derived hypothesis that a named company exists at a
    given website, prior to any Tavily verification call. It must never be
    constructed from an unverified assumption that the source URL's domain
    is the company's official website — ``website`` here is only ever a
    *candidate* website, subject to identity verification downstream.
    """

    company_name: str
    website: str | None
    title: str
    content: str
    source_url: str
    source: str = "public_web_search"
    discovery_metadata: list[dict[str, object]] = field(default_factory=list)

    @property
    def canonical_name(self) -> str:
        return " ".join(self.company_name.casefold().split())

    @property
    def canonical_domain(self) -> str | None:
        if not self.website:
            return None
        domain = urlparse(self.website).netloc.casefold().removeprefix("www.")
        return domain or None
