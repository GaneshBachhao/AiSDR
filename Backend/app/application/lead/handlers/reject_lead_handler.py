"""Reject Lead application handler."""

from __future__ import annotations

from app.application.common.exceptions.conflict_exception import ConflictException
from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.common.interfaces.unit_of_work import UnitOfWork
from app.application.lead.dto.lead_responses import LeadResponseDTO
from app.application.lead.lead_commands import RejectLeadCommand
from app.application.lead.lead_mapper import LeadMapper
from app.domain.lead.identifiers.lead_id import LeadId


class RejectLeadHandler:
    """Reject a pending-review Lead. Can be resubmitted afterward."""

    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self._unit_of_work = unit_of_work

    async def handle(self, command: RejectLeadCommand) -> LeadResponseDTO:
        async with self._unit_of_work:
            lead = await self._unit_of_work.lead_repository.get_by_id(
                LeadId(command.lead_id),
            )

            if lead is None:
                raise NotFoundException(
                    message="Lead not found.",
                    details={"lead_id": command.lead_id},
                )

            try:
                lead.reject(notes=command.notes)
            except ValueError as exc:
                raise ConflictException(
                    message=str(exc),
                    details={"lead_id": command.lead_id},
                ) from exc

            await self._unit_of_work.lead_repository.update(lead)
            await self._unit_of_work.commit()

        return LeadMapper.to_response(lead)
