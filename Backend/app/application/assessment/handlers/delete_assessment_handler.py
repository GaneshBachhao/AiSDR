"""
Delete Assessment handler.
"""

from __future__ import annotations

from app.application.assessment.assessment_commands import (
    DeleteAssessmentCommand,
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


class DeleteAssessmentHandler:
    """
    Handle Delete Assessment use case.
    """

    def __init__(
        self,
        unit_of_work: UnitOfWork,
    ) -> None:
        self._unit_of_work = unit_of_work

    async def handle(
        self,
        command: DeleteAssessmentCommand | str,
    ) -> None:
        """
        Delete an assessment.
        """

        assessment_id = command.assessment_id if isinstance(command, DeleteAssessmentCommand) else command

        async with self._unit_of_work:
            assessment = await self._unit_of_work.assessment_repository.get_by_id(
                AssessmentId(assessment_id),
            )

            if assessment is None:
                raise NotFoundException(
                    message="Assessment not found.",
                    details={
                        "assessment_id": assessment_id,
                    },
                )

            await self._unit_of_work.assessment_repository.delete(
                assessment,
            )
