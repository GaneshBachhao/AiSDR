import pytest

from app.domain.company_research.value_objects.domain_profile import DomainProfile
from app.infrastructure.configuration.domain_profiles import (
    load_all_domain_profiles,
    load_domain_profile,
)

EXPECTED_SECTORS = {
    "manufacturing",
    "healthcare",
    "pharma",
    "biotech",
    "research",
    "logistics",
    "financial services",
    "construction",
    "retail",
}


def test_load_all_domain_profiles_covers_the_nine_initial_sectors():
    profiles = load_all_domain_profiles()
    assert set(profiles.keys()) == EXPECTED_SECTORS


@pytest.mark.parametrize("sector", sorted(EXPECTED_SECTORS))
def test_load_domain_profile_returns_a_populated_profile(sector):
    profile = load_domain_profile(sector)
    assert isinstance(profile, DomainProfile)
    assert profile.name == sector
    assert profile.industry_keywords
    assert profile.negative_service_markers
    assert profile.enterprise_exclusion_markers


def test_load_domain_profile_is_case_and_whitespace_insensitive():
    assert load_domain_profile(" Manufacturing ").name == "manufacturing"


def test_load_domain_profile_raises_for_unknown_sector():
    with pytest.raises(ValueError, match="No domain profile found"):
        load_domain_profile("underwater basket weaving")
