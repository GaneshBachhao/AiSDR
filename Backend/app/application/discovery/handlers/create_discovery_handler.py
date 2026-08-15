"""Create Discovery application handler."""

from __future__ import annotations

from sqlalchemy.exc import IntegrityError

from app.application.common.exceptions.conflict_exception import ConflictException
from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.common.exceptions.validation_exception import ValidationException
from app.application.common.interfaces.unit_of_work import UnitOfWork
from app.application.discovery.discovery_commands import CreateDiscoveryCommand
from app.application.discovery.discovery_mapper import DiscoveryMapper
from app.application.discovery.discovery_validator import DiscoveryValidator
from app.application.discovery.dto.discovery_responses import DiscoveryResponseDTO
from app.domain.discovery.entities.discovery import Discovery
from app.domain.lead.identifiers.lead_id import LeadId


class CreateDiscoveryHandler:
    """Handle the Create Discovery use case."""

    def __init__(
        self,
        unit_of_work: UnitOfWork,
        validator: DiscoveryValidator,
        mapper: DiscoveryMapper,
    ) -> None:
        self._unit_of_work = unit_of_work
        self._validator = validator
        self._mapper = mapper

    async def handle(self, command: CreateDiscoveryCommand) -> DiscoveryResponseDTO:
        validation = self._validator.validate_create(command)
        if not validation.is_valid:
            raise ValidationException(
                message="Discovery validation failed.",
                details={error.field: error.message for error in validation.errors},
            )

        try:
            lead_id = LeadId(command.lead_id)
        except (TypeError, ValueError) as exc:
            raise ValidationException(
                message="Discovery validation failed.",
                details={"lead_id": str(exc)},
            ) from exc

        discovery = Discovery(
            lead_id=lead_id,
            problem_statement=command.problem_statement,
            current_solution=command.current_solution,
            business_impact=command.business_impact,
            success_criteria=command.success_criteria,
        )

        try:
            async with self._unit_of_work:
                lead = await self._unit_of_work.lead_repository.get_by_id(lead_id)
                if lead is None:
                    raise NotFoundException(
                        message="Lead not found.",
                        details={"lead_id": command.lead_id},
                    )

                existing = await self._unit_of_work.discovery_repository.get_by_lead(lead_id)
                if existing is not None:
                    raise ConflictException(
                        message="Discovery already exists for this lead.",
                        details={"lead_id": command.lead_id},
                    )

                await self._unit_of_work.discovery_repository.add(discovery)
                await self._unit_of_work.commit()
        except IntegrityError as exc:
            raise ConflictException(
                message="Unable to create discovery.",
                details={"lead_id": command.lead_id},
            ) from exc

        return self._mapper.to_response_dto(discovery)
