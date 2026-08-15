from app.domain.company_research.services.qualification_scorer import (
    QualificationScorer,
    ScoringInputs,
)


def _inputs(**overrides):
    defaults = dict(
        signals={"hiring": False, "growth": False, "technology": False, "ai": False, "process": False, "funding": False},
        evidence_count=0,
        website_verified=False,
        services_matched=False,
        scale_signal="none",
    )
    defaults.update(overrides)
    return ScoringInputs(**defaults)


def test_business_fit_rewards_service_match():
    matched = QualificationScorer.score(_inputs(services_matched=True))
    unmatched = QualificationScorer.score(_inputs(services_matched=False))
    assert matched.business_fit == QualificationScorer.BUSINESS_FIT_MATCH
    assert unmatched.business_fit == QualificationScorer.BUSINESS_FIT_NO_MATCH


def test_evidence_strength_requires_both_evidence_and_confirmed_signal():
    strong = QualificationScorer.score(_inputs(evidence_count=2, signals={"hiring": True}))
    weak_no_signal = QualificationScorer.score(_inputs(evidence_count=2, signals={"hiring": False}))
    weak_no_evidence = QualificationScorer.score(_inputs(evidence_count=0, signals={"hiring": True}))
    assert strong.evidence_strength == QualificationScorer.EVIDENCE_STRONG
    assert weak_no_signal.evidence_strength == QualificationScorer.EVIDENCE_WEAK
    assert weak_no_evidence.evidence_strength == QualificationScorer.EVIDENCE_WEAK


def test_buying_signal_present_for_hiring_growth_or_funding():
    for key in ("hiring", "growth", "funding"):
        score = QualificationScorer.score(_inputs(signals={key: True}))
        assert score.buying_signal == QualificationScorer.BUYING_SIGNAL_PRESENT


def test_ability_scales_with_scale_signal():
    strong = QualificationScorer.score(_inputs(scale_signal="strong"))
    moderate = QualificationScorer.score(_inputs(scale_signal="moderate"))
    none_ = QualificationScorer.score(_inputs(scale_signal="none"))
    assert strong.ability == QualificationScorer.ABILITY_STRONG
    assert moderate.ability == QualificationScorer.ABILITY_MODERATE
    assert none_.ability == QualificationScorer.ABILITY_NONE


def test_accessibility_requires_verified_website():
    with_site = QualificationScorer.score(_inputs(website_verified=True))
    without_site = QualificationScorer.score(_inputs(website_verified=False))
    assert with_site.accessibility == QualificationScorer.ACCESSIBILITY_WITH_WEBSITE
    assert without_site.accessibility == QualificationScorer.ACCESSIBILITY_WITHOUT_WEBSITE


def test_full_strong_profile_reaches_tier_a():
    score = QualificationScorer.score(
        _inputs(
            signals={"hiring": True, "technology": True},
            evidence_count=3,
            website_verified=True,
            services_matched=True,
            scale_signal="strong",
        )
    )
    assert score.tier == "Tier A"
