from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse

from app.company_research.funnel.candidate import DiscoveryCandidate
from app.company_research.funnel.normalizer import CandidateNormalizer


@dataclass(slots=True)
class GateDecision:
    accepted: bool
    reason: str


class DeterministicCandidateGate:
    """Hard gate for cheap checks that must run before paid verification/research."""

    DEFAULT_BLOCKED_DOMAINS = frozenset(
        {
            "wikipedia.org", "linkedin.com", "facebook.com", "youtube.com",
            "twitter.com", "x.com", "instagram.com", "indiamart.com",
            "tradeindia.com", "justdial.com", "sulekha.com", "scribd.com", "simplyhired.co.in", "indeed.com", "glassdoor.co.in", "glassdoor.com",
        }
    )
    DEFAULT_BLOCKED_EXTENSIONS = frozenset(
        {".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx", ".zip", ".rar"}
    )
    DEFAULT_BLOCKED_TITLE_MARKERS = (
        "top 10", "top 20", "list of", "directory", "market report", "industry report",
        "press release", "news", "blog", "article", "whitepaper", "brochure",
    )

    def __init__(
        self,
        blocked_domains: frozenset[str] | None = None,
        blocked_title_markers: tuple[str, ...] | None = None,
    ) -> None:
        self.blocked_domains = blocked_domains or self.DEFAULT_BLOCKED_DOMAINS
        self.blocked_title_markers = blocked_title_markers or self.DEFAULT_BLOCKED_TITLE_MARKERS

    def evaluate(self, candidate: DiscoveryCandidate) -> GateDecision:
        name = candidate.company_name.strip()
        title = candidate.title.strip().casefold()
        url = candidate.website or candidate.source_url
        if not name:
            return GateDecision(False, "missing_company_name")
        if not url:
            return GateDecision(False, "missing_url")

        parsed = urlparse(url)
        domain = parsed.netloc.casefold().removeprefix("www.")
        if not domain:
            return GateDecision(False, "invalid_domain")
        if any(domain == item or domain.endswith("." + item) for item in self.blocked_domains):
            return GateDecision(False, "blocked_domain")
        if any(parsed.path.casefold().endswith(ext) for ext in self.DEFAULT_BLOCKED_EXTENSIONS):
            return GateDecision(False, "blocked_document")
        if any(marker in title for marker in self.blocked_title_markers):
            return GateDecision(False, "non_company_result_title")
        if len(name) < 3 or len(name) > 120:
            return GateDecision(False, "invalid_company_name_length")
        return GateDecision(True, "accepted")

    def accept_unique(self, candidates: list[DiscoveryCandidate]) -> list[DiscoveryCandidate]:
        accepted: list[DiscoveryCandidate] = []
        seen: set[str] = set()
        for candidate in candidates:
            decision = self.evaluate(candidate)
            if not decision.accepted:
                continue
            key = CandidateNormalizer.canonical_key(candidate)
            if key in seen:
                continue
            seen.add(key)
            accepted.append(candidate)
        return accepted
