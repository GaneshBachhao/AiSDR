"""Record Sequence Bounce application handler."""

from __future__ import annotations

from app.application.common.exceptions.conflict_exception import ConflictException
from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.common.interfaces.unit_of_work import UnitOfWork
from app.application.sequence.dto.sequence_responses import SequenceResponseDTO
from app.application.sequence.sequence_commands import RecordSequenceBounceCommand
from app.application.sequence.sequence_mapper import SequenceMapper
from app.domain.sequence.identifiers.sequence_id import SequenceId


class RecordSequenceBounceHandler:
    """Stop a Sequence early: a touch bounced.

    No automated caller exists yet -- there is no real channel adapter
    (EPIC-09.3) to report a bounce. Operator/test triggered via the API
    today.
    """

    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self._unit_of_work = unit_of_work

    async def handle(self, command: RecordSequenceBounceCommand) -> SequenceResponseDTO:
        sequence_id = SequenceId(command.sequence_id)

        async with self._unit_of_work:
            sequence = await self._unit_of_work.sequence_repository.get_by_id(sequence_id)
            if sequence is None:
                raise NotFoundException(
                    message="Sequence not found.",
                    details={"sequence_id": command.sequence_id},
                )

            try:
                sequence.record_bounce()
            except ValueError as exc:
                raise ConflictException(
                    message=str(exc),
                    details={"sequence_id": command.sequence_id},
                ) from exc

            await self._unit_of_work.sequence_repository.update(sequence)
            await self._unit_of_work.commit()

        return SequenceMapper.to_response(sequence)
