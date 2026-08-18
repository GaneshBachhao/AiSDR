import pytest

from app.domain.company_research.value_objects.domain_profile import DomainProfile


def test_requires_a_name():
    with pytest.raises(ValueError, match="name is required"):
        DomainProfile(name="")


def test_requires_a_non_whitespace_name():
    with pytest.raises(ValueError, match="name is required"):
        DomainProfile(name="   ")


def test_requires_a_positive_enterprise_exclusion_threshold():
    with pytest.raises(ValueError, match="must be positive"):
        DomainProfile(name="custom", enterprise_exclusion_threshold=0)


def test_defaults_are_inert():
    profile = DomainProfile(name="empty")
    assert profile.industry_keywords == {}
    assert profile.negative_service_markers == ()
    assert profile.enterprise_exclusion_threshold == 1000
    assert profile.enterprise_exclusion_markers == ()
    assert profile.evidence_scope_keywords == ()
    assert profile.scoring_weight_overrides == {}


def test_is_frozen():
    profile = DomainProfile(name="custom")
    with pytest.raises(AttributeError):
        profile.name = "other"  # type: ignore[misc]
