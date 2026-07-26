"""
Handler for discovering companies.
"""

from __future__ import annotations

from app.application.discovery.validators.discover_companies_validator import (
    DiscoverCompaniesValidator,
)
from app.application.discovery.commands.discover_companies import (
    DiscoverCompaniesCommand,
)
from app.application.discovery.dto.discovery_dto import DiscoveryDTO
from app.application.discovery.mappers.discovery_mapper import DiscoveryMapper


class DiscoverCompaniesHandler:
    """
    Executes company discovery workflow.
    """

    def __init__(
        self,
        discovery_service,
        validator: DiscoverCompaniesValidator | None = None,
    ):
        self._discovery_service = discovery_service
        self._validator = validator or DiscoverCompaniesValidator()

    def handle(
        self,
        command: DiscoverCompaniesCommand,
    ):

        validation = self._validator.validate(command)

        if not validation.success:
            return validation

        results = self._discovery_service.discover(
            command.industry,
            command.location,
            command.max_results,
        )

        return DiscoveryMapper.results_to_response(results)