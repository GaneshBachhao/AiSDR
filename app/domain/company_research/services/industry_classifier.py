from __future__ import annotations


class IndustryClassifier:
    """Deterministic, keyword-based industry inference and matching.

    Network-free by design: operates only on text already gathered by
    discovery/evidence adapters. Not a substitute for identity verification —
    this answers "what industry does the evidence suggest", not "is this
    really the company we think it is".
    """

    INDUSTRY_KEYWORDS = {
        "manufacturing": (
            "manufacturer", "manufacturing", "factory", "production plant",
            "industrial machinery", "industrial equipment", "automotive manufacturer",
            "electronics manufacturing", "component manufacturer", "fabrication",
            "machinery maker", "production facility",
        ),
        "information technology": (
            "software company", "software development", "it services", "information technology",
            "technology services", "saas", "software as a service", "cloud services",
            "systems integrator", "managed services", "technology consulting",
        ),
        "software": (
            "software company", "software development", "saas", "software platform",
            "enterprise software", "software products",
        ),
        "healthcare": (
            "healthcare provider", "healthcare company", "hospital", "clinic", "health system",
            "patient care", "medical center",
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
        "telecommunications": ("telecommunications", "telecom", "mobile network", "internet service provider"),
        "education": ("university", "college", "education provider", "school", "edtech"),
        "research": ("research institute", "research organization", "laboratory", "r&d center"),
    }

    NEGATIVE_SERVICE_MARKERS = (
        "it services", "software company", "software development", "technology consulting",
        "ai company", "automation vendor", "cloud consulting", "digital agency",
        "system integrator", "managed services", "staffing", "recruitment agency",
    )

    @classmethod
    def infer_industry(
        cls,
        text: str,
        title: str,
        targets: list[str],
    ) -> str | None:
        haystack = f"{title} {text}".lower()
        best_target = None
        best_score = 0
        for target in targets or cls.INDUSTRY_KEYWORDS.keys():
            keywords = cls.INDUSTRY_KEYWORDS.get(target.lower(), (target.lower(),))
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
    ) -> tuple[bool, str]:
        if not targets:
            return True, "No industry restriction was requested."
        normalized_targets = [t.lower().strip() for t in targets]
        normalized_industry = (industry or "").lower()
        for target in normalized_targets:
            if normalized_industry and (target in normalized_industry or normalized_industry in target):
                return True, f"Primary industry is consistent with requested industry: {target}."
            keywords = cls.INDUSTRY_KEYWORDS.get(target, (target,))
            positive = sum(1 for word in keywords if word in text)
            negative = sum(1 for word in cls.NEGATIVE_SERVICE_MARKERS if word in text)
            if positive >= 2 and positive > negative:
                return True, f"Public company information contains multiple signals consistent with {target}."
        return False, "Public information does not sufficiently support the requested industry."
