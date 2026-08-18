"""Update Discovery application handler."""

from __future__ import annotations

from sqlalchemy.exc import IntegrityError

from app.application.common.exceptions.not_found_exception import (
    NotFoundException,
)
from app.application.common.exceptions.validation_exception import (
    ValidationException,
)
from app.application.common.interfaces.unit_of_work import UnitOfWork
from app.application.discovery.discovery_commands import UpdateDiscoveryCommand
from app.application.discovery.discovery_mapper import DiscoveryMapper
from app.application.discovery.discovery_validator import DiscoveryValidator
from app.application.discovery.dto.discovery_responses import (
    DiscoveryResponseDTO,
)
from app.domain.discovery.enums.discovery_status import DiscoveryStatus
from app.domain.discovery.identifiers.discovery_id import DiscoveryId


class UpdateDiscoveryHandler:
    """Handle the Update Discovery use case."""

    def __init__(
        self,
        unit_of_work: UnitOfWork,
        validator: DiscoveryValidator,
        mapper: DiscoveryMapper,
    ) -> None:
        self._unit_of_work = unit_of_work
        self._validator = validator
        self._mapper = mapper

    async def handle(
        self,
        command: UpdateDiscoveryCommand,
    ) -> DiscoveryResponseDTO:
        validation = self._validator.validate_update(command)

        if not validation.is_valid:
            raise ValidationException(
                message="Discovery validation failed.",
                details={error.field: error.message for error in validation.errors},
            )

        try:
            discovery_id = DiscoveryId(command.discovery_id)
        except (TypeError, ValueError) as exc:
            raise ValidationException(
                message="Discovery validation failed.",
                details={
                    "discovery_id": str(exc),
                },
            ) from exc

        async with self._unit_of_work:
            discovery = await self._unit_of_work.discovery_repository.get_by_id(discovery_id)

            if discovery is None:
                raise NotFoundException(
                    message="Discovery session not found.",
                    details={
                        "discovery_id": command.discovery_id,
                    },
                )

            # -------------------------------------------------
            # Update discovery details
            # -------------------------------------------------

            discovery.update_details(
                problem_statement=command.problem_statement,
                current_solution=command.current_solution,
                business_impact=command.business_impact,
                success_criteria=command.success_criteria,
            )

            # -------------------------------------------------
            # Update lifecycle status
            # -------------------------------------------------

            if command.status is not None:
                status = DiscoveryStatus(command.status.strip().upper())

                discovery.update_status(status)

            # -------------------------------------------------
            # Persist
            # -------------------------------------------------

            try:
                await self._unit_of_work.discovery_repository.update(discovery)

                await self._unit_of_work.commit()

            except IntegrityError as exc:
                raise ValidationException(
                    message="Unable to update discovery.",
                    details={
                        "discovery_id": command.discovery_id,
                    },
                ) from exc

        return self._mapper.to_response_dto(discovery)
