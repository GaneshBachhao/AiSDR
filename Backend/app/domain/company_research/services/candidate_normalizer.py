from __future__ import annotations

import re
from urllib.parse import urlparse, urlunparse

from app.domain.company_research.entities.candidate import CompanyCandidate


class CandidateNormalizer:
    """Normalizes company identity without network or LLM calls.

    This is the deterministic half of entity resolution: turning
    "ABC Pvt Ltd" / "ABC Private Limited" / "ABC PVT. LTD." into a
    comparable key. It intentionally does not attempt legal-suffix-aware
    fuzzy matching yet — that arrives with identity verification (Phase 2)
    where a wrong-domain match (e.g. a generic word matching an unrelated
    parent company's domain) must be actively guarded against, not just
    normalized past.
    """

    @staticmethod
    def normalize_name(value: str) -> str:
        value = re.sub(r"[^a-z0-9]+", " ", value.casefold())
        return " ".join(value.split())

    @staticmethod
    def normalize_root_url(value: str | None) -> str | None:
        if not value:
            return None
        parsed = urlparse(value.strip())
        if not parsed.netloc:
            return None
        scheme = parsed.scheme or "https"
        domain = parsed.netloc.casefold().removeprefix("www.")
        return urlunparse((scheme, domain, "", "", "", ""))

    @classmethod
    def canonical_key(cls, candidate: CompanyCandidate) -> str:
        domain = candidate.canonical_domain
        if domain:
            return f"domain:{domain}"
        return f"name:{cls.normalize_name(candidate.company_name)}"
