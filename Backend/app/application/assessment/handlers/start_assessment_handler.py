"""
Start Assessment handler.
"""

from __future__ import annotations

from app.application.assessment.assessment_commands import (
    StartAssessmentCommand,
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


class StartAssessmentHandler:
    """
    Handle Start Assessment use case.
    """

    def __init__(
        self,
        unit_of_work: UnitOfWork,
    ) -> None:
        self._unit_of_work = unit_of_work

    async def handle(
        self,
        command: StartAssessmentCommand,
    ) -> GetAssessmentResponseDTO:
        """
        Start assessment workflow.
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

            assessment.start()

            await self._unit_of_work.assessment_repository.update(
                assessment,
            )
            await self._unit_of_work.commit()

        return AssessmentMapper.to_get_response(
            assessment,
        )
