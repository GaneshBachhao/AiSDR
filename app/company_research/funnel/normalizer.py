from __future__ import annotations

import re
from urllib.parse import urlparse, urlunparse

from app.company_research.funnel.candidate import DiscoveryCandidate


class CandidateNormalizer:
    """Normalizes company identity without network or LLM calls."""

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
    def canonical_key(cls, candidate: DiscoveryCandidate) -> str:
        domain = candidate.canonical_domain
        if domain:
            return f"domain:{domain}"
        return f"name:{cls.normalize_name(candidate.company_name)}"
