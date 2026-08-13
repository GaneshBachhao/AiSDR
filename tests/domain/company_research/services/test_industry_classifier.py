from app.domain.company_research.services.industry_classifier import IndustryClassifier
from app.domain.company_research.value_objects.domain_profile import DomainProfile


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


def test_default_behavior_is_unchanged_when_no_profile_is_passed():
    """Regression guard: omitting ``profile`` must behave exactly as before
    Domain Profiles existed."""
    text = "Acme is a leading manufacturer of industrial machinery and components."
    with_default = IndustryClassifier.infer_industry(text, "Acme Manufacturing", ["Manufacturing"])
    explicit_none = IndustryClassifier.infer_industry(
        text, "Acme Manufacturing", ["Manufacturing"], profile=None
    )
    assert with_default == explicit_none == "Manufacturing"


def test_custom_profile_keywords_override_the_defaults():
    profile = DomainProfile(
        name="custom",
        industry_keywords={"widgets": ("widget maker", "widget factory")},
    )
    # "manufacturer" alone means nothing under the custom vocabulary...
    industry = IndustryClassifier.infer_industry(
        "Acme is a manufacturer.", "Acme", ["widgets"], profile=profile
    )
    assert industry is None

    # ...but the profile's own keyword does.
    industry = IndustryClassifier.infer_industry(
        "Acme is a widget maker and widget factory.", "Acme", ["widgets"], profile=profile
    )
    assert industry == "widgets"


def test_custom_profile_negative_markers_override_the_defaults():
    profile = DomainProfile(
        name="custom",
        industry_keywords={"manufacturing": ("manufacturer", "factory")},
        negative_service_markers=("consulting shop", "advisory firm"),
    )

    # Custom negative markers suppress the match when they outweigh the positives.
    text = "acme is a manufacturer with a factory, but also a consulting shop and advisory firm"
    matched, _ = IndustryClassifier.matches(None, text, ["manufacturing"], profile=profile)
    assert matched is False

    # The default negative marker ("it services") is irrelevant to this
    # profile -- it no longer suppresses the match.
    text_with_default_marker = "acme is a manufacturer with a factory, also an it services shop"
    matched, _ = IndustryClassifier.matches(
        None, text_with_default_marker, ["manufacturing"], profile=profile
    )
    assert matched is True
