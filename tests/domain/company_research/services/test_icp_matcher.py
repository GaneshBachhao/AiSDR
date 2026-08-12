from app.domain.company_research.services.icp_matcher import IcpMatcher


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
    assert IcpMatcher.company_size_label(600) == "500+"
