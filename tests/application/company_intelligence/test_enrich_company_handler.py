"""
Unit Tests for EnrichCompanyHandler
"""

from app.application.company_intelligence.commands.enrich_company import (
    EnrichCompanyCommand,
)

from app.application.company_intelligence.handlers.enrich_company_handler import (
    EnrichCompanyHandler,
)

from app.company_intelligence.schemas.company_profile_schema import (
    CompanyProfile,
)


class FakeCompanyIntelligenceService:

    def enrich(
        self,
        candidate,
    ):

        return CompanyProfile(

            company_name=candidate.company_name,

            website=str(candidate.website),

            source="fake",
        )


def test_handler_returns_success():

    handler = EnrichCompanyHandler(

        company_service=FakeCompanyIntelligenceService(),
    )

    command = EnrichCompanyCommand(

        company_name="OpenAI",

        website="https://openai.com",

        source="test",
    )

    result = handler.handle(command)

    assert result.success

    assert result.data.company_name == "OpenAI"