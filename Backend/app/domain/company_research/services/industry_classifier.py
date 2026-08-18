from __future__ import annotations

from app.domain.company_research.value_objects.domain_profile import DomainProfile


class IndustryClassifier:
    """Deterministic, keyword-based industry inference and matching.

    Network-free by design: operates only on text already gathered by
    discovery/evidence adapters. Not a substitute for identity verification —
    this answers "what industry does the evidence suggest", not "is this
    really the company we think it is".

    Accepts an optional ``DomainProfile`` to override the vocabulary below
    per-sector. When omitted, behavior is unchanged from before Domain
    Profiles existed -- the class constants below remain the single source
    of truth for the default profile.
    """

    INDUSTRY_KEYWORDS = {
        "manufacturing": (
            "manufacturer",
            "manufacturing",
            "factory",
            "production plant",
            "industrial machinery",
            "industrial equipment",
            "automotive manufacturer",
            "electronics manufacturing",
            "component manufacturer",
            "fabrication",
            "machinery maker",
            "production facility",
        ),
        "information technology": (
            "software company",
            "software development",
            "it services",
            "information technology",
            "technology services",
            "saas",
            "software as a service",
            "cloud services",
            "systems integrator",
            "managed services",
            "technology consulting",
        ),
        "software": (
            "software company",
            "software development",
            "saas",
            "software platform",
            "enterprise software",
            "software products",
        ),
        "healthcare": (
            "healthcare provider",
            "healthcare company",
            "hospital",
            "clinic",
            "health system",
            "patient care",
            "medical center",
        ),
        "hospitals": ("hospital", "medical center", "health system"),
        "pharma": ("pharmaceutical", "pharma", "biotechnology", "biotech", "drug manufacturer"),
        "biotechnology": ("biotechnology", "biotech", "life sciences"),
        "financial services": ("bank", "banking", "financial services", "fintech", "lending"),
        "insurance": ("insurance company", "insurer", "insurance provider"),
        "logistics": ("logistics", "freight", "transportation", "warehousing", "supply chain"),
        "retail": ("retailer", "retail company", "e-commerce", "ecommerce", "online retailer"),
        "real estate": ("real estate", "property developer", "property management", "realty"),
        "construction": ("construction company", "contractor", "engineering and construction"),
        "travel": ("travel company", "tour operator", "travel agency", "hospitality"),
        "hospitality": ("hotel", "hospitality", "resort", "restaurant group"),
        "energy": ("energy company", "utility", "power generation", "renewable energy", "oil and gas"),
        "agriculture": ("agriculture", "agricultural", "agribusiness", "farm", "crop producer"),
        "telecommunications": (
            "telecommunications",
            "telecom",
            "mobile network",
            "internet service provider",
        ),
        "education": ("university", "college", "education provider", "school", "edtech"),
        "research": ("research institute", "research organization", "laboratory", "r&d center"),
    }

    NEGATIVE_SERVICE_MARKERS = (
        "it services",
        "software company",
        "software development",
        "technology consulting",
        "ai company",
        "automation vendor",
        "cloud consulting",
        "digital agency",
        "system integrator",
        "managed services",
        "staffing",
        "recruitment agency",
    )

    @classmethod
    def _keywords(cls, profile: DomainProfile | None) -> dict[str, tuple[str, ...]]:
        if profile is not None and profile.industry_keywords:
            return profile.industry_keywords
        return cls.INDUSTRY_KEYWORDS

    @classmethod
    def _negative_markers(cls, profile: DomainProfile | None) -> tuple[str, ...]:
        if profile is not None and profile.negative_service_markers:
            return profile.negative_service_markers
        return cls.NEGATIVE_SERVICE_MARKERS

    @classmethod
    def infer_industry(
        cls,
        text: str,
        title: str,
        targets: list[str],
        profile: DomainProfile | None = None,
    ) -> str | None:
        industry_keywords = cls._keywords(profile)
        haystack = f"{title} {text}".lower()
        best_target = None
        best_score = 0
        for target in targets or industry_keywords.keys():
            keywords = industry_keywords.get(target.lower(), (target.lower(),))
            score = sum(1 for word in keywords if word in haystack)
            if score > best_score:
                best_score = score
                best_target = target
        return best_target if best_score else None

    @classmethod
    def matches(
        cls,
        industry: str | None,
        text: str,
        targets: list[str],
        profile: DomainProfile | None = None,
    ) -> tuple[bool, str]:
        if not targets:
            return True, "No industry restriction was requested."
        industry_keywords = cls._keywords(profile)
        negative_markers = cls._negative_markers(profile)
        normalized_targets = [t.lower().strip() for t in targets]
        normalized_industry = (industry or "").lower()
        for target in normalized_targets:
            if normalized_industry and (target in normalized_industry or normalized_industry in target):
                return True, f"Primary industry is consistent with requested industry: {target}."
            keywords = industry_keywords.get(target, (target,))
            positive = sum(1 for word in keywords if word in text)
            negative = sum(1 for word in negative_markers if word in text)
            if positive >= 2 and positive > negative:
                return True, f"Public company information contains multiple signals consistent with {target}."
        return False, "Public information does not sufficiently support the requested industry."
