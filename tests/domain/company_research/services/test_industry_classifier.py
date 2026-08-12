from app.domain.company_research.services.industry_classifier import IndustryClassifier


def test_infers_manufacturing_from_keywords():
    industry = IndustryClassifier.infer_industry(
        "Acme is a leading manufacturer of industrial machinery and components.",
        "Acme Manufacturing",
        ["Manufacturing"],
    )
    assert industry == "Manufacturing"


def test_infer_returns_none_without_keyword_hits():
    industry = IndustryClassifier.infer_industry("A generic page with no industry signal.", "Acme", ["Manufacturing"])
    assert industry is None


def test_matches_true_when_no_industries_requested():
    matched, reason = IndustryClassifier.matches(None, "", [])
    assert matched is True
    assert "No industry restriction" in reason


def test_matches_true_on_direct_industry_name_overlap():
    matched, reason = IndustryClassifier.matches("Manufacturing", "some text", ["Manufacturing"])
    assert matched is True
    assert "consistent with requested industry" in reason


def test_matches_true_on_sufficient_keyword_density():
    text = "acme is a manufacturer operating a large factory and production plant"
    matched, _ = IndustryClassifier.matches(None, text, ["Manufacturing"])
    assert matched is True


def test_matches_false_when_evidence_is_insufficient():
    matched, reason = IndustryClassifier.matches(None, "a small local bakery", ["Manufacturing"])
    assert matched is False
    assert "does not sufficiently support" in reason


def test_negative_markers_suppress_a_weak_match():
    text = "we are an it services and software development company, not a manufacturer"
    matched, _ = IndustryClassifier.matches(None, text, ["Manufacturing"])
    assert matched is False
