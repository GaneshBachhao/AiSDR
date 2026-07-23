"""
Unit Tests for DiscoveryMapper
"""

from app.application.discovery.commands.discover_companies import (
    DiscoverCompaniesCommand,
)

from app.application.discovery.mappers.discovery_mapper import (
    DiscoveryMapper,
)

from app.discovery.schemas.discovery_schema import (
    DiscoveryResult,
)


def test_command_to_dto():

    command = DiscoverCompaniesCommand(

        industry="Healthcare",

        location="India",

        max_results=5,
    )

    dto = DiscoveryMapper.command_to_dto(command)

    assert dto.industry == command.industry

    assert dto.location == command.location

    assert dto.max_results == command.max_results


def test_results_to_response():

    results = [

        DiscoveryResult(

            company_name="ABC",

            source="Manual",
        )
    ]

    response = DiscoveryMapper.results_to_response(results)

    assert len(response.companies) == 1

    assert response.companies[0].company_name == "ABC"