"""List OutcomeEvents application handler."""

from __future__ import annotations

from app.application.common.interfaces.unit_of_work import UnitOfWork
from app.application.outcome.dto.outcome_responses import OutcomeEventResponseDTO
from app.application.outcome.outcome_mapper import OutcomeMapper
from app.domain.lead.identifiers.lead_id import LeadId


class ListOutcomeEventsHandler:
    """List outcome events, optionally filtered to one Lead."""

    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self._unit_of_work = unit_of_work

    async def handle(
        self,
        lead_id: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[OutcomeEventResponseDTO]:
        async with self._unit_of_work:
            if lead_id is not None:
                events = await self._unit_of_work.outcome_repository.list_by_lead(LeadId(lead_id))
            else:
                events = await self._unit_of_work.outcome_repository.list(skip=skip, limit=limit)

        return OutcomeMapper.to_response_list(events)
