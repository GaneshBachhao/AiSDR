from __future__ import annotations

from urllib.parse import urlparse

from app.domain.company_research.entities.candidate import CompanyCandidate
from app.domain.company_research.services.candidate_normalizer import CandidateNormalizer
from app.domain.company_research.value_objects.gate_decision import GateDecision


class DeterministicCandidateGate:
    """Hard gate for cheap checks that must run before paid verification/research.

    Every rule here is deterministic and network-free by design: this gate
    exists precisely so that directory pages, social profiles, documents,
    and article-style titles never reach the expensive identity-verification
    or research stages. No LLM call belongs in this class.
    """

    DEFAULT_BLOCKED_DOMAINS = frozenset(
        {
            "wikipedia.org", "linkedin.com", "facebook.com", "youtube.com",
            "twitter.com", "x.com", "instagram.com", "indiamart.com",
            "tradeindia.com", "justdial.com", "sulekha.com", "scribd.com",
            "simplyhired.co.in", "indeed.com", "glassdoor.co.in", "glassdoor.com",
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

    def evaluate(self, candidate: CompanyCandidate) -> GateDecision:
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

    def accept_unique(self, candidates: list[CompanyCandidate]) -> list[CompanyCandidate]:
        accepted: list[CompanyCandidate] = []
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
