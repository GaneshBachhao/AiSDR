"""
Unit Tests for DiscoverCompaniesHandler
"""

from app.application.discovery.commands.discover_companies import (
    DiscoverCompaniesCommand,
)

from app.application.discovery.handlers.discover_companies_handler import (
    DiscoverCompaniesHandler,
)

from app.discovery.schemas.discovery_schema import (
    DiscoveryResult,
)


class FakeDiscoveryService:

    def discover(self, request):

        return [

            DiscoveryResult(

                company_name="OpenAI",

                source="Test",
            )
        ]


def test_handler_returns_success():

    handler = DiscoverCompaniesHandler(

        discovery_service=FakeDiscoveryService(),
    )

    command = DiscoverCompaniesCommand(

        industry="AI",

        location="USA",

        max_results=5,
    )

    result = handler.handle(command)

    assert result.success

    assert len(result.data.companies) == 1

    assert result.data.companies[0].company_name == "OpenAI"