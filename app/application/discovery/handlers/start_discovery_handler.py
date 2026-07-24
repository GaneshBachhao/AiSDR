"""
Start Discovery application handler.
"""

from __future__ import annotations

from app.application.contracts.repositories.discovery_repository import (
    DiscoveryRepository,
)

from app.application.discovery.commands.start_discovery import (
    StartDiscoveryCommand,
)

from app.application.discovery.dto.discovery_dto import (
    DiscoveryDTO,
)

from app.application.discovery.mappers.discovery_mapper import (
    DiscoveryMapper,
)

from app.application.discovery.validators.start_discovery_validator import (
    StartDiscoveryValidator,
)

from app.domain.discovery.entities.discovery_session import (
    DiscoverySession,
)

from app.domain.discovery.services.discovery_service import (
    DiscoveryService,
)

from app.domain.lead.identifiers.lead_id import (
    LeadId,
)


class StartDiscoveryHandler:
    """
    Handles starting a discovery session.
    """

    def __init__(
        self,
        repository: DiscoveryRepository,
        validator: StartDiscoveryValidator,
        mapper: DiscoveryMapper,
    ):
        self._repository = repository
        self._validator = validator
        self._mapper = mapper

    async def handle(
        self,
        command: StartDiscoveryCommand,
    ) -> DiscoveryDTO:

        validation = self._validator.validate(command)

        if not validation.is_valid:
            raise ValueError(validation.errors)

        session = DiscoverySession(
            lead_id=LeadId(
                command.lead_id
            ),
            company_id=command.company_id,
        )

        DiscoveryService.start(session)

        await self._repository.add(session)

        return self._mapper.to_dto(session)