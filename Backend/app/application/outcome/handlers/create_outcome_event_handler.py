"""Create OutcomeEvent application handler."""

from __future__ import annotations

from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.common.interfaces.unit_of_work import UnitOfWork
from app.application.outcome.dto.outcome_responses import OutcomeEventResponseDTO
from app.application.outcome.outcome_commands import CreateOutcomeEventCommand
from app.application.outcome.outcome_mapper import OutcomeMapper
from app.domain.lead.identifiers.lead_id import LeadId


class CreateOutcomeEventHandler:
    """Record an outcome for a Lead.

    Not idempotent -- unlike suppression, this is an append-only log. Two
    "No Response" events for the same Lead a week apart are both real
    facts, not a duplicate to collapse.
    """

    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self._unit_of_work = unit_of_work

    async def handle(self, command: CreateOutcomeEventCommand) -> OutcomeEventResponseDTO:
        lead_id = LeadId(command.lead_id)

        async with self._unit_of_work:
            lead = await self._unit_of_work.lead_repository.get_by_id(lead_id)
            if lead is None:
                raise NotFoundException(
                    message="Lead not found.",
                    details={"lead_id": command.lead_id},
                )

            event = OutcomeMapper.to_domain(command)
            await self._unit_of_work.outcome_repository.add(event)
            await self._unit_of_work.commit()

        return OutcomeMapper.to_response(event)
