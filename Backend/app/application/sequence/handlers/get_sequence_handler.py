"""Get Sequence application handler."""

from __future__ import annotations

from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.common.interfaces.unit_of_work import UnitOfWork
from app.application.sequence.dto.sequence_responses import SequenceResponseDTO
from app.application.sequence.sequence_mapper import SequenceMapper
from app.domain.sequence.identifiers.sequence_id import SequenceId


class GetSequenceHandler:
    """Get a Sequence by ID."""

    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self._unit_of_work = unit_of_work

    async def handle(self, sequence_id: str) -> SequenceResponseDTO:
        async with self._unit_of_work:
            sequence = await self._unit_of_work.sequence_repository.get_by_id(SequenceId(sequence_id))

        if sequence is None:
            raise NotFoundException(
                message="Sequence not found.",
                details={"sequence_id": sequence_id},
            )

        return SequenceMapper.to_response(sequence)
