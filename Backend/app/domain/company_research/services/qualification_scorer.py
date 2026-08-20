from __future__ import annotations

from dataclasses import dataclass

from app.domain.company_research.services.icp_matcher import IcpMatcher
from app.domain.company_research.value_objects.qualification_score import QualificationScore


@dataclass(slots=True, frozen=True)
class ScoringInputs:
    """Everything the deterministic scorer needs; no network, no request/DTO coupling."""

    signals: dict[str, bool]
    evidence_count: int
    website_verified: bool
    services_matched: bool
    employee_count: int | None


class QualificationScorer:
    """Deterministic, weighted qualification scoring.

    Weights mirror the original single-provider implementation:
    business fit (23/14), evidence strength (22/7), buying signal (17/6),
    ability-to-pay scale (10/9/7/5/3/4-unknown, see
    ``IcpMatcher.size_score``), accessibility (9/4).
    """

    BUSINESS_FIT_MATCH = 23
    BUSINESS_FIT_NO_MATCH = 14

    EVIDENCE_STRONG = 22
    EVIDENCE_WEAK = 7

    BUYING_SIGNAL_PRESENT = 17
    BUYING_SIGNAL_ABSENT = 6

    ACCESSIBILITY_WITH_WEBSITE = 9
    ACCESSIBILITY_WITHOUT_WEBSITE = 4

    @classmethod
    def score(
        cls,
        inputs: ScoringInputs,
        weight_overrides: dict[str, float] | None = None,
    ) -> QualificationScore:
        """Score ``inputs``, optionally recalibrated per Domain Profile.

        ``weight_overrides`` maps the same keys as
        ``DomainProfile.scoring_weight_overrides`` (EPIC-12) onto any of
        this class's 8 point constants -- e.g. ``{"business_fit_match":
        30}``. Omitted keys, and the default ``None``, fall back to the
        class constants below, so every existing caller behaves exactly as
        before.
        """
        weights = cls._resolve_weights(weight_overrides)

        has_confirmed_signal = any(inputs.signals.values())
        has_evidence = inputs.evidence_count > 0 and has_confirmed_signal

        business_fit = (
            weights["business_fit_match"] if inputs.services_matched else weights["business_fit_no_match"]
        )
        evidence_strength = weights["evidence_strong"] if has_evidence else weights["evidence_weak"]
        buying_signal = (
            weights["buying_signal_present"]
            if (inputs.signals.get("hiring") or inputs.signals.get("growth") or inputs.signals.get("funding"))
            else weights["buying_signal_absent"]
        )
        # Ability-to-pay is now driven by the ICP's own company-size point
        # table (docs/company_search_and_prompt_tuning.md §1b) applied to
        # the actually-extracted employee count, not by whether evidence
        # text happens to mention scale-sounding keywords ("employees",
        # "revenue", "million"...) -- that heuristic rewarded *any*
        # mention of scale, including describing a company as
        # enterprise-sized, which is backwards for a 5-1,000 employee ICP.
        ability = IcpMatcher.size_score(inputs.employee_count)
        accessibility = (
            weights["accessibility_with_website"]
            if inputs.website_verified
            else weights["accessibility_without_website"]
        )

        return QualificationScore(
            business_fit=business_fit,
            evidence_strength=evidence_strength,
            buying_signal=buying_signal,
            ability=ability,
            accessibility=accessibility,
        )

    @classmethod
    def _resolve_weights(cls, weight_overrides: dict[str, float] | None) -> dict[str, int]:
        defaults = {
            "business_fit_match": cls.BUSINESS_FIT_MATCH,
            "business_fit_no_match": cls.BUSINESS_FIT_NO_MATCH,
            "evidence_strong": cls.EVIDENCE_STRONG,
            "evidence_weak": cls.EVIDENCE_WEAK,
            "buying_signal_present": cls.BUYING_SIGNAL_PRESENT,
            "buying_signal_absent": cls.BUYING_SIGNAL_ABSENT,
            "accessibility_with_website": cls.ACCESSIBILITY_WITH_WEBSITE,
            "accessibility_without_website": cls.ACCESSIBILITY_WITHOUT_WEBSITE,
        }
        if not weight_overrides:
            return defaults
        return {
            key: int(round(weight_overrides[key])) if key in weight_overrides else default
            for key, default in defaults.items()
        }
