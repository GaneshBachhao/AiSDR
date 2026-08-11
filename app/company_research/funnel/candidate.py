from __future__ import annotations

from dataclasses import dataclass, field
from urllib.parse import urlparse


@dataclass(slots=True)
class DiscoveryCandidate:
    """Cheap, normalized company candidate used before paid verification/research."""

    company_name: str
    website: str | None
    title: str
    content: str
    source_url: str
    source: str = "public_web_search"
    discovery_metadata: list[dict] = field(default_factory=list)

    @property
    def canonical_name(self) -> str:
        return " ".join(self.company_name.casefold().split())

    @property
    def canonical_domain(self) -> str | None:
        if not self.website:
            return None
        domain = urlparse(self.website).netloc.casefold().removeprefix("www.")
        return domain or None
