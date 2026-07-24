"""
Complete Discovery application handler.
"""

from __future__ import annotations

from app.application.contracts.repositories.discovery_repository import (
    DiscoveryRepository,
)

from app.application.discovery.commands.complete_discovery import (
    CompleteDiscoveryCommand,
)

from app.application.discovery.dto.discovery_dto import (
    DiscoveryDTO,
)

from app.application.discovery.mappers.discovery_mapper import (
    DiscoveryMapper,
)

from app.application.discovery.validators.complete_discovery_validator import (
    CompleteDiscoveryValidator,
)

from app.domain.discovery.identifiers.discovery_session_id import (
    DiscoverySessionId,
)


class CompleteDiscoveryHandler:
    """
    Handles completion of discovery sessions.
    """

    def __init__(
        self,
        repository: DiscoveryRepository,
        validator: CompleteDiscoveryValidator,
        mapper: DiscoveryMapper,
    ):
        self._repository = repository
        self._validator = validator
        self._mapper = mapper

    async def handle(
        self,
        command: CompleteDiscoveryCommand,
    ) -> DiscoveryDTO:

        validation = self._validator.validate(command)

        if not validation.is_valid:
            raise ValueError(validation.errors)

        session = await self._repository.get_by_id(
            DiscoverySessionId(
                command.discovery_session_id
            )
        )

        if session is None:
            raise ValueError(
                "Discovery session not found."
            )

        session.complete(
            command.summary
        )

        await self._repository.update(
            session
        )

        return self._mapper.to_dto(
            session
        )