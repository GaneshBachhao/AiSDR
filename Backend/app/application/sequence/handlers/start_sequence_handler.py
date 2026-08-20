"""Start Sequence application handler."""

from __future__ import annotations

from app.application.common.exceptions.conflict_exception import ConflictException
from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.common.interfaces.unit_of_work import UnitOfWork
from app.application.sequence.dto.sequence_responses import SequenceResponseDTO
from app.application.sequence.sequence_commands import StartSequenceCommand
from app.application.sequence.sequence_mapper import SequenceMapper
from app.domain.lead.enums.lead_review_status import LeadReviewStatus
from app.domain.sequence.identifiers.sequence_id import SequenceId


class StartSequenceHandler:
    """Begin a Sequence's touch cadence.

    The first real caller of EPIC-16's review gate: nothing in this
    codebase could yet check `Lead.review_status == APPROVED` before this
    handler existed, even though EPIC-16's own Risk Register note already
    named this exact requirement for whenever EPIC-09 built a real
    trigger point. There is still no real send mechanism (EPIC-09.3)
    downstream of this -- but this is the first real gate on the actual
    entry point into the send pipeline, not a placeholder.
    """

    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self._unit_of_work = unit_of_work

    async def handle(self, command: StartSequenceCommand) -> SequenceResponseDTO:
        sequence_id = SequenceId(command.sequence_id)

        async with self._unit_of_work:
            sequence = await self._unit_of_work.sequence_repository.get_by_id(sequence_id)
            if sequence is None:
                raise NotFoundException(
                    message="Sequence not found.",
                    details={"sequence_id": command.sequence_id},
                )

            lead = await self._unit_of_work.lead_repository.get_by_id(sequence.lead_id)
            if lead is None:
                raise NotFoundException(
                    message="Lead not found.",
                    details={"lead_id": str(sequence.lead_id)},
                )

            if lead.review_status != LeadReviewStatus.APPROVED:
                raise ConflictException(
                    message="Lead must be approved via the review gate before starting a Sequence.",
                    details={
                        "lead_id": str(sequence.lead_id),
                        "review_status": lead.review_status.value,
                    },
                )

            try:
                sequence.start()
            except ValueError as exc:
                raise ConflictException(
                    message=str(exc),
                    details={"sequence_id": command.sequence_id},
                ) from exc

            await self._unit_of_work.sequence_repository.update(sequence)
            await self._unit_of_work.commit()

        return SequenceMapper.to_response(sequence)
