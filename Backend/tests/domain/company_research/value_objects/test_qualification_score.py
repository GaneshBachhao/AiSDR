from app.domain.company_research.value_objects.qualification_score import QualificationScore


def test_total_sums_components():
    score = QualificationScore(
        business_fit=23, evidence_strength=22, buying_signal=17, ability=12, accessibility=9
    )
    assert score.total == 83


def test_total_is_clamped_to_100():
    score = QualificationScore(
        business_fit=23, evidence_strength=22, buying_signal=17, ability=12, accessibility=99
    )
    assert score.total == 100


def test_tier_a_threshold():
    score = QualificationScore(
        business_fit=23, evidence_strength=22, buying_signal=17, ability=12, accessibility=9
    )
    assert score.tier == "Tier A"


def test_tier_b_threshold():
    score = QualificationScore(
        business_fit=14, evidence_strength=22, buying_signal=17, ability=7, accessibility=4
    )
    assert score.tier == "Tier B"


def test_tier_c_threshold():
    score = QualificationScore(
        business_fit=14, evidence_strength=7, buying_signal=6, ability=9, accessibility=4
    )
    assert score.tier == "Tier C"


def test_not_qualified_below_threshold():
    score = QualificationScore(
        business_fit=14, evidence_strength=7, buying_signal=6, ability=4, accessibility=4
    )
    assert score.tier == "Not qualified"
