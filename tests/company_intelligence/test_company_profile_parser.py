import pytest

from app.company_intelligence.parsers.company_profile_parser import (
    CompanyProfileParser,
)

from app.company_intelligence.schemas.company_profile_schema import (
    CompanyProfile,
)


# ---------------------------------------------------------
# Valid JSON
# ---------------------------------------------------------

def test_parse_valid_json():

    response = """
    {
        "company_name": "ABC Manufacturing",
        "website": "https://abc.com",
        "industry": "Manufacturing",
        "employee_count": 120
    }
    """

    profile = CompanyProfileParser.parse(response)

    assert isinstance(profile, CompanyProfile)

    assert profile.company_name == "ABC Manufacturing"

    assert profile.website == "https://abc.com"

    assert profile.industry == "Manufacturing"

    assert profile.employee_count == 120


# ---------------------------------------------------------
# Markdown JSON
# ---------------------------------------------------------

def test_parse_markdown_json():

    response = """
            ```json
            {
                "company_name": "XYZ Industries",
                "website": "https://xyz.com"
            }"""
    