"""
Unit Tests for CompanyProfileMapper
"""

from app.application.company_intelligence.commands.enrich_company import (
    EnrichCompanyCommand,
)

from app.application.company_intelligence.mappers.company_profile_mapper import (
    CompanyProfileMapper,
)

from app.company_intelligence.schemas.company_profile_schema import (
    CompanyProfile,
)


def test_command_to_candidate():

    command = EnrichCompanyCommand(

        company_name="OpenAI",

        website="https://openai.com",

        source="test",
    )

    dto = CompanyProfileMapper.command_to_dto(
        command,
    )

    candidate = CompanyProfileMapper.dto_to_candidate(
        dto,
    )

    assert candidate.company_name == "OpenAI"

    assert str(candidate.website) == "https://openai.com/"


def test_profile_to_response():

    profile = CompanyProfile(

        company_name="OpenAI",

        website="https://openai.com",

        source="gemini",
    )

    response = CompanyProfileMapper.profile_to_response(
        profile,
    )

    assert response.company_name == "OpenAI"

    assert response.website == "https://openai.com"