from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class QualificationScore:
    """Deterministic breakdown of a company's qualification score.

    Each component is a pre-weighted point contribution (not a 0-1 ratio),
    so ``total`` is a plain sum clamped to the public 0-100 scale used by
    ``CompanySearchResult.qualification_score``.
    """

    business_fit: int
    evidence_strength: int
    buying_signal: int
    ability: int
    accessibility: int

    TIER_A_THRESHOLD = 80
    TIER_B_THRESHOLD = 60
    TIER_C_THRESHOLD = 40

    @property
    def total(self) -> int:
        return min(
            100,
            self.business_fit
            + self.evidence_strength
            + self.buying_signal
            + self.ability
            + self.accessibility,
        )

    @property
    def tier(self) -> str:
        total = self.total
        if total >= self.TIER_A_THRESHOLD:
            return "Tier A"
        if total >= self.TIER_B_THRESHOLD:
            return "Tier B"
        if total >= self.TIER_C_THRESHOLD:
            return "Tier C"
        return "Not qualified"
