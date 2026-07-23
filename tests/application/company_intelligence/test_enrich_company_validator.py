"""
Unit Tests for EnrichCompanyValidator
"""

from app.application.company_intelligence.validators.enrich_company_validator import (
    EnrichCompanyValidator,
)

from app.lead_intelligence.schemas.lead_candidate_schema import (
    LeadCandidate,
)


def test_validator_accepts_valid_candidate():

    validator = EnrichCompanyValidator()

    candidate = LeadCandidate(

        company_name="OpenAI",

        website="https://openai.com",

        source="unit-test",
    )

    result = validator.validate(candidate)

    assert result.success

    assert result.errors == []


def test_validator_requires_company_name():

    validator = EnrichCompanyValidator()

    candidate = LeadCandidate(

        company_name="",

        website="https://openai.com",

        source="unit-test",
    )

    result = validator.validate(candidate)

    assert not result.success

    assert "Company name is required." in result.errors


def test_validator_requires_website():

    validator = EnrichCompanyValidator()

    candidate = LeadCandidate(

        company_name="OpenAI",

        website=None,

        source="unit-test",
    )

    result = validator.validate(candidate)

    assert not result.success

    assert "Website is required." in result.errors