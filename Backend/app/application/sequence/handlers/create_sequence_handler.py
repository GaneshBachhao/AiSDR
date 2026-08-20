"""Create Sequence application handler."""

from __future__ import annotations

from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.common.exceptions.validation_exception import ValidationException
from app.application.common.interfaces.unit_of_work import UnitOfWork
from app.application.sequence.dto.sequence_responses import SequenceResponseDTO
from app.application.sequence.sequence_commands import CreateSequenceCommand
from app.application.sequence.sequence_mapper import SequenceMapper
from app.domain.lead.identifiers.lead_id import LeadId


class CreateSequenceHandler:
    """Create a planned touch cadence for a Lead."""

    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self._unit_of_work = unit_of_work

    async def handle(self, command: CreateSequenceCommand) -> SequenceResponseDTO:
        try:
            sequence = SequenceMapper.to_domain(command)
        except (TypeError, ValueError) as exc:
            raise ValidationException(
                message="Sequence validation failed.",
                details={"error": str(exc)},
            ) from exc

        async with self._unit_of_work:
            lead = await self._unit_of_work.lead_repository.get_by_id(LeadId(command.lead_id))
            if lead is None:
                raise NotFoundException(
                    message="Lead not found.",
                    details={"lead_id": command.lead_id},
                )

            await self._unit_of_work.sequence_repository.add(sequence)
            await self._unit_of_work.commit()

        return SequenceMapper.to_response(sequence)
