from __future__ import annotations


class EvidenceSignalExtractor:
    """Deterministic buying-signal detection and evidence classification.

    Evidence classification follows the four tiers defined in
    ``docs/adr/AiSDR_master_instructions.md`` §9: Confirmed Need, Strong
    Opportunity Signal, Reasonable Business Hypothesis, and Unverified
    Assumption. An assumption must never be presented as a confirmed fact,
    so "Unverified Assumption" is only used when there is genuinely no
    supporting evidence at all.
    """

    SIGNAL_KEYWORDS = {
        "hiring": ("hiring", "careers", "job opening", "vacancy", "recruiting"),
        "growth": ("expansion", "expanded", "acquisition", "funding", "investment", "new location", "growth"),
        "technology": ("cloud", "azure", "software", "technology", "digital", "data", "erp", "crm", "modernization", "migration"),
        "ai": ("artificial intelligence", "generative ai", "machine learning", "ai ", "automation", "copilot"),
        "process": ("manual process", "workflow", "documents", "reporting", "compliance", "operations", "integration"),
        "funding": ("funding", "investment", "raised", "series a", "series b", "grant"),
    }

    SCALE_STRONG_MARKERS = ("enterprise", "employees", "revenue", "funding", "investment", "million", "billion")
    SCALE_MODERATE_MARKERS = ("established", "global company", "large company")

    @classmethod
    def extract_signals(cls, combined_text: str) -> dict[str, bool]:
        return {
            name: any(keyword in combined_text for keyword in keywords)
            for name, keywords in cls.SIGNAL_KEYWORDS.items()
        }

    @staticmethod
    def trigger_event(signals: dict[str, bool]) -> str | None:
        events = []
        if signals.get("hiring"):
            events.append("technology hiring")
        if signals.get("growth"):
            events.append("growth / expansion")
        if signals.get("funding"):
            events.append("funding / investment")
        return ", ".join(events) if events else None

    @classmethod
    def scale_signal(cls, combined_text: str) -> str:
        if any(marker in combined_text for marker in cls.SCALE_STRONG_MARKERS):
            return "strong"
        if any(marker in combined_text for marker in cls.SCALE_MODERATE_MARKERS):
            return "moderate"
        return "none"

    @staticmethod
    def classify_scope(text: str, company_name: str) -> str:
        """Return "company_specific" if ``text`` plausibly refers to the
        named company, else "industry_general".

        A cheap, deterministic proxy for whether a search result actually
        surfaced company-specific evidence versus topically-related
        industry noise -- Tavily's queries are built with the company name
        as a search term, but a search engine can still return generic
        articles that merely rank well for that query.
        """
        normalized_name = company_name.strip().lower()
        normalized_text = text.lower()
        if not normalized_name:
            return "industry_general"
        if normalized_name in normalized_text:
            return "company_specific"
        # Tolerate legal-suffix variation ("Acme Manufacturing" vs.
        # "Acme Manufacturing Pvt Ltd") by also matching on the first
        # significant word of the name.
        first_word = normalized_name.split()[0]
        if len(first_word) >= 4 and first_word in normalized_text:
            return "company_specific"
        return "industry_general"

    @staticmethod
    def classify_evidence(
        signals: dict[str, bool],
        evidence_count: int,
        company_specific_signals: dict[str, bool] | None = None,
        company_specific_evidence_count: int = 0,
    ) -> str:
        """Classify overall evidence strength.

        ``Confirmed Need`` requires the confirmed signals to actually come
        from company-specific evidence, not merely from the combined text
        (which may include industry-general noise). Callers that don't pass
        ``company_specific_signals``/``company_specific_evidence_count``
        can never reach ``Confirmed Need`` -- unknown scope is treated
        conservatively, not permissively.
        """
        confirmed = sum(1 for value in signals.values() if value)
        confirmed_company_specific = sum(
            1 for value in (company_specific_signals or {}).values() if value
        )

        if (
            confirmed >= 2
            and evidence_count >= 3
            and confirmed_company_specific >= 2
            and company_specific_evidence_count >= 2
        ):
            return "Confirmed Need"
        if confirmed >= 1 and evidence_count >= 1:
            return "Strong Opportunity Signal"
        if evidence_count >= 1:
            return "Reasonable Business Hypothesis"
        return "Unverified Assumption"
