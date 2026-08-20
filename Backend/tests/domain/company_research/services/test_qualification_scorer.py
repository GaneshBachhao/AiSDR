from app.domain.company_research.services.icp_matcher import IcpMatcher
from app.domain.company_research.services.qualification_scorer import (
    QualificationScorer,
    ScoringInputs,
)


def _inputs(**overrides):
    defaults = dict(
        signals={
            "hiring": False,
            "growth": False,
            "technology": False,
            "ai": False,
            "process": False,
            "funding": False,
        },
        evidence_count=0,
        website_verified=False,
        services_matched=False,
        employee_count=None,
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


def test_ability_scales_with_employee_count_via_the_icp_size_score_table():
    small = QualificationScorer.score(_inputs(employee_count=50))
    mid = QualificationScorer.score(_inputs(employee_count=800))
    large = QualificationScorer.score(_inputs(employee_count=5000))
    unknown = QualificationScorer.score(_inputs(employee_count=None))
    assert small.ability == IcpMatcher.size_score(50)
    assert mid.ability == IcpMatcher.size_score(800)
    assert large.ability == IcpMatcher.size_score(5000)
    assert unknown.ability == IcpMatcher.size_score(None)


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
            employee_count=50,
        )
    )
    assert score.tier == "Tier A"


def test_none_weight_overrides_preserves_default_output():
    without_overrides = QualificationScorer.score(_inputs(services_matched=True))
    with_none = QualificationScorer.score(_inputs(services_matched=True), weight_overrides=None)
    assert with_none == without_overrides


def test_empty_weight_overrides_preserves_default_output():
    without_overrides = QualificationScorer.score(_inputs(services_matched=True))
    with_empty = QualificationScorer.score(_inputs(services_matched=True), weight_overrides={})
    assert with_empty == without_overrides


def test_weight_overrides_can_replace_a_single_constant():
    score = QualificationScorer.score(
        _inputs(services_matched=True),
        weight_overrides={"business_fit_match": 30},
    )
    assert score.business_fit == 30
    assert score.accessibility == QualificationScorer.ACCESSIBILITY_WITHOUT_WEBSITE


def test_weight_overrides_can_replace_every_constant():
    score = QualificationScorer.score(
        _inputs(
            signals={"hiring": True},
            evidence_count=2,
            website_verified=True,
            services_matched=True,
            employee_count=50,
        ),
        weight_overrides={
            "business_fit_match": 30,
            "business_fit_no_match": 10,
            "evidence_strong": 25,
            "evidence_weak": 5,
            "buying_signal_present": 20,
            "buying_signal_absent": 5,
            "accessibility_with_website": 12,
            "accessibility_without_website": 2,
        },
    )
    assert score.business_fit == 30
    assert score.evidence_strength == 25
    assert score.buying_signal == 20
    assert score.accessibility == 12


def test_weight_overrides_rounds_float_values_to_int_points():
    score = QualificationScorer.score(
        _inputs(services_matched=True),
        weight_overrides={"business_fit_match": 30.6},
    )
    assert score.business_fit == 31
