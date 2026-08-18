"""List Discovery application handler."""

from __future__ import annotations

from app.application.common.exceptions.validation_exception import ValidationException
from app.application.common.interfaces.unit_of_work import UnitOfWork
from app.application.discovery.discovery_mapper import DiscoveryMapper
from app.application.discovery.discovery_queries import ListDiscoveryQuery
from app.application.discovery.discovery_validator import DiscoveryValidator
from app.application.discovery.dto.discovery_responses import DiscoveryResponseDTO


class ListDiscoveryHandler:
    """Handle the List Discoveries use case."""

    def __init__(
        self, unit_of_work: UnitOfWork, validator: DiscoveryValidator, mapper: DiscoveryMapper
    ) -> None:
        self._unit_of_work = unit_of_work
        self._validator = validator
        self._mapper = mapper

    async def handle(self, query: ListDiscoveryQuery) -> list[DiscoveryResponseDTO]:
        validation = self._validator.validate_list(query)
        if not validation.is_valid:
            raise ValidationException(
                message="Discovery validation failed.",
                details={error.field: error.message for error in validation.errors},
            )

        async with self._unit_of_work:
            discoveries = await self._unit_of_work.discovery_repository.list(
                skip=query.skip,
                limit=query.limit,
            )

        return self._mapper.to_response_list(discoveries)
