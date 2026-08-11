"""
Get Assessment handler.
"""

from __future__ import annotations

from app.application.assessment.assessment_mapper import (
    AssessmentMapper,
)
from app.application.assessment.assessment_queries import (
    GetAssessmentQuery,
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


class GetAssessmentHandler:
    """
    Handle Get Assessment use case.
    """

    def __init__(
        self,
        unit_of_work: UnitOfWork,
    ) -> None:
        self._unit_of_work = unit_of_work

    async def handle(
        self,
        query: GetAssessmentQuery,
    ) -> GetAssessmentResponseDTO:
        """
        Retrieve an assessment by identifier.
        """

        async with self._unit_of_work:
            assessment = await self._unit_of_work.assessment_repository.get_by_id(
                AssessmentId(query.assessment_id),
            )

            if assessment is None:
                raise NotFoundException(
                    message="Assessment not found.",
                    details={
                        "assessment_id": query.assessment_id,
                    },
                )

        return AssessmentMapper.to_get_response(
            assessment,
        )