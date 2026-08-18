from app.domain.company_research.services.icp_matcher import IcpMatcher
from app.domain.company_research.value_objects.domain_profile import DomainProfile


def test_extract_employee_count_from_explicit_phrase():
    assert IcpMatcher.extract_employee_count("The company has approximately 120 employees.") == 120


def test_extract_employee_count_handles_thousands_separator():
    assert IcpMatcher.extract_employee_count("Headcount: 1,250 employees") == 1250


def test_extract_employee_count_returns_none_when_absent():
    assert IcpMatcher.extract_employee_count("No workforce information here.") is None


def test_size_range_recognizes_named_bands():
    assert IcpMatcher.size_range("SMB") == (21, 500)
    assert IcpMatcher.size_range("startup") == (1, 20)
    assert IcpMatcher.size_range("enterprise") == (501, 10_000_000)


def test_size_range_recognizes_explicit_numeric_range():
    assert IcpMatcher.size_range("50-200") == (50, 200)


def test_matches_size_true_with_no_restriction():
    matched, count, reason = IcpMatcher.matches_size("no employee info", [])
    assert matched is True
    assert count is None
    assert "No company-size restriction" in reason


def test_matches_size_false_when_employee_count_unknown_but_restricted():
    matched, count, reason = IcpMatcher.matches_size("a growing company", ["SMB"])
    assert matched is False
    assert count is None
    assert "explicit size evidence" in reason


def test_matches_size_true_within_requested_range():
    matched, count, _ = IcpMatcher.matches_size("the company has 120 employees", ["SMB"])
    assert matched is True
    assert count == 120


def test_matches_size_false_outside_requested_range():
    matched, count, _ = IcpMatcher.matches_size("the company has 5000 employees", ["SMB"])
    assert matched is False
    assert count == 5000


def test_enterprise_exclusion_by_employee_count():
    excluded, parent = IcpMatcher.enterprise_exclusion("", 5000)
    assert excluded is True
    assert parent is None


def test_enterprise_exclusion_by_explicit_marker():
    excluded, _ = IcpMatcher.enterprise_exclusion("a fortune 500 company", None)
    assert excluded is True


def test_enterprise_exclusion_extracts_parent_company_without_excluding():
    excluded, parent = IcpMatcher.enterprise_exclusion(
        "Lathangi Motors is a subsidiary of Example Holdings Group", None
    )
    assert excluded is False
    assert parent == "Example Holdings Group"


def test_company_size_label_bands():
    assert IcpMatcher.company_size_label(None) is None
    assert IcpMatcher.company_size_label(10) == "Startup / Micro"
    assert IcpMatcher.company_size_label(600) == "501-1,000"
    assert IcpMatcher.company_size_label(1200) == "1,000+"


def test_enterprise_exclusion_default_behavior_unchanged_when_no_profile_passed():
    """Regression guard: omitting ``profile`` must behave exactly as before
    Domain Profiles existed."""
    with_default = IcpMatcher.enterprise_exclusion("", 1001)
    explicit_none = IcpMatcher.enterprise_exclusion("", 1001, profile=None)
    assert with_default == explicit_none == (True, None)


def test_enterprise_exclusion_profile_can_raise_the_threshold():
    profile = DomainProfile(name="custom", enterprise_exclusion_threshold=2000)
    # 1001 employees would exclude under the default (1000) threshold...
    excluded, _ = IcpMatcher.enterprise_exclusion("", 1001)
    assert excluded is True
    # ...but not under a profile that raises the threshold.
    excluded, _ = IcpMatcher.enterprise_exclusion("", 1001, profile=profile)
    assert excluded is False


def test_size_score_matches_the_icp_point_table():
    # docs/company_search_and_prompt_tuning.md §1b
    assert IcpMatcher.size_score(5) == 10
    assert IcpMatcher.size_score(100) == 10
    assert IcpMatcher.size_score(150) == 9
    assert IcpMatcher.size_score(500) == 7
    assert IcpMatcher.size_score(1000) == 5
    assert IcpMatcher.size_score(1500) == 3


def test_size_score_unknown_employee_count_is_conservative_not_a_guess():
    assert IcpMatcher.size_score(None) == 4


def test_enterprise_exclusion_profile_can_replace_explicit_markers():
    profile = DomainProfile(
        name="custom",
        enterprise_exclusion_markers=("state-owned enterprise",),
    )
    # The default marker ("fortune 500") no longer applies under this profile.
    excluded, _ = IcpMatcher.enterprise_exclusion("a fortune 500 company", None, profile=profile)
    assert excluded is False
    # The profile's own marker does.
    excluded, _ = IcpMatcher.enterprise_exclusion("a state-owned enterprise", None, profile=profile)
    assert excluded is True
