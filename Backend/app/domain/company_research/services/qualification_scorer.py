from __future__ import annotations

from dataclasses import dataclass

from app.domain.company_research.value_objects.qualification_score import QualificationScore


@dataclass(slots=True, frozen=True)
class ScoringInputs:
    """Everything the deterministic scorer needs; no network, no request/DTO coupling."""

    signals: dict[str, bool]
    evidence_count: int
    website_verified: bool
    services_matched: bool
    scale_signal: str


class QualificationScorer:
    """Deterministic, weighted qualification scoring.

    Weights mirror the original single-provider implementation:
    business fit (23/14), evidence strength (22/7), buying signal (17/6),
    ability-to-pay scale (12/7/4), accessibility (9/4).
    """

    BUSINESS_FIT_MATCH = 23
    BUSINESS_FIT_NO_MATCH = 14

    EVIDENCE_STRONG = 22
    EVIDENCE_WEAK = 7

    BUYING_SIGNAL_PRESENT = 17
    BUYING_SIGNAL_ABSENT = 6

    ABILITY_STRONG = 12
    ABILITY_MODERATE = 7
    ABILITY_NONE = 4

    ACCESSIBILITY_WITH_WEBSITE = 9
    ACCESSIBILITY_WITHOUT_WEBSITE = 4

    @classmethod
    def score(cls, inputs: ScoringInputs) -> QualificationScore:
        has_confirmed_signal = any(inputs.signals.values())
        has_evidence = inputs.evidence_count > 0 and has_confirmed_signal

        business_fit = cls.BUSINESS_FIT_MATCH if inputs.services_matched else cls.BUSINESS_FIT_NO_MATCH
        evidence_strength = cls.EVIDENCE_STRONG if has_evidence else cls.EVIDENCE_WEAK
        buying_signal = (
            cls.BUYING_SIGNAL_PRESENT
            if (inputs.signals.get("hiring") or inputs.signals.get("growth") or inputs.signals.get("funding"))
            else cls.BUYING_SIGNAL_ABSENT
        )
        ability = {
            "strong": cls.ABILITY_STRONG,
            "moderate": cls.ABILITY_MODERATE,
        }.get(inputs.scale_signal, cls.ABILITY_NONE)
        accessibility = (
            cls.ACCESSIBILITY_WITH_WEBSITE if inputs.website_verified else cls.ACCESSIBILITY_WITHOUT_WEBSITE
        )

        return QualificationScore(
            business_fit=business_fit,
            evidence_strength=evidence_strength,
            buying_signal=buying_signal,
            ability=ability,
            accessibility=accessibility,
        )
