"""
Add Discovery Response application handler.
"""

from __future__ import annotations

from app.application.contracts.repositories.discovery_repository import (
    DiscoveryRepository,
)

from app.application.discovery.commands.add_discovery_response import (
    AddDiscoveryResponseCommand,
)

from app.application.discovery.dto.discovery_response_dto import (
    DiscoveryResponseDTO,
)

from app.application.discovery.mappers.discovery_response_mapper import (
    DiscoveryResponseMapper,
)

from app.application.discovery.validators.add_discovery_response_validator import (
    AddDiscoveryResponseValidator,
)

from app.domain.discovery.entities.discovery_response import (
    DiscoveryResponse,
)

from app.domain.discovery.identifiers.discovery_session_id import (
    DiscoverySessionId,
)

from app.domain.discovery.enums.response_type import (
    ResponseType,
)


class AddDiscoveryResponseHandler:
    """
    Handles adding responses to discovery sessions.
    """

    def __init__(
        self,
        repository: DiscoveryRepository,
        validator: AddDiscoveryResponseValidator,
        mapper: DiscoveryResponseMapper,
    ):
        self._repository = repository
        self._validator = validator
        self._mapper = mapper

    async def handle(
        self,
        command: AddDiscoveryResponseCommand,
    ) -> DiscoveryResponseDTO:

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

        response = DiscoveryResponse(
            question_id=command.question_id,
            question=command.question,
            answer=command.answer,
            response_type=ResponseType(
                command.response_type
            ),
            confidence=command.confidence,
            remarks=command.remarks,
        )

        session.add_response(response)

        await self._repository.update(session)

        return self._mapper.to_dto(response)