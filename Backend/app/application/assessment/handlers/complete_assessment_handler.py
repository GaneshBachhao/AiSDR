"""
Complete Assessment handler.

Wires the domain's existing `Assessment.complete()` lifecycle method
(stamps `completed_at`, sets `status = COMPLETED`) to a real endpoint.
Previously, assessment completion was only reachable indirectly through
the generic PUT /assessments/{id} update endpoint, which never called
complete() and so never stamped completed_at -- a caller had to set
status="Completed" by hand and get completed_at wrong.
"""

from __future__ import annotations

from app.application.assessment.assessment_commands import (
    CompleteAssessmentCommand,
)
from app.application.assessment.assessment_mapper import (
    AssessmentMapper,
)
from app.application.assessment.dto.assessment_response import (
    GetAssessmentResponseDTO,
)
from app.application.common.exceptions.not_found_exception import (
    NotFoundException,
)
from app.application.common.interfaces.unit_of_work import (
    UnitOfWork,
)
from app.domain.assessment.identifiers.assessment_id import (
    AssessmentId,
)


class CompleteAssessmentHandler:
    """
    Handle Complete Assessment use case.
    """

    def __init__(
        self,
        unit_of_work: UnitOfWork,
    ) -> None:
        self._unit_of_work = unit_of_work

    async def handle(
        self,
        command: CompleteAssessmentCommand,
    ) -> GetAssessmentResponseDTO:
        """
        Complete assessment workflow.
        """

        async with self._unit_of_work:
            assessment = await self._unit_of_work.assessment_repository.get_by_id(
                AssessmentId(
                    command.assessment_id,
                ),
            )

            if assessment is None:
                raise NotFoundException(
                    message="Assessment not found.",
                    details={
                        "assessment_id": command.assessment_id,
                    },
                )

            assessment.complete(summary=command.summary)

            await self._unit_of_work.assessment_repository.update(
                assessment,
            )
            await self._unit_of_work.commit()

        return AssessmentMapper.to_get_response(
            assessment,
        )
