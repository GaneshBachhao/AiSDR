"""List Sequences application handler."""

from __future__ import annotations

from app.application.common.interfaces.unit_of_work import UnitOfWork
from app.application.sequence.dto.sequence_responses import SequenceResponseDTO
from app.application.sequence.sequence_mapper import SequenceMapper
from app.domain.lead.identifiers.lead_id import LeadId


class ListSequencesHandler:
    """List Sequences for one Lead."""

    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self._unit_of_work = unit_of_work

    async def handle(self, lead_id: str) -> list[SequenceResponseDTO]:
        async with self._unit_of_work:
            sequences = await self._unit_of_work.sequence_repository.list_by_lead(LeadId(lead_id))

        return SequenceMapper.to_response_list(sequences)
