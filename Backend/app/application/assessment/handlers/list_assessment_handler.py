"""
List Assessment handler.
"""

from __future__ import annotations

from app.application.assessment.assessment_mapper import (
    AssessmentMapper,
)
from app.application.assessment.assessment_queries import (
    ListAssessmentsQuery,
)
from app.application.assessment.dto.assessment_response import (
    ListAssessmentResponseDTO,
)
from app.application.common.interfaces.unit_of_work import (
    UnitOfWork,
)


class ListAssessmentHandler:
    """
    Handle List Assessment use case.
    """

    def __init__(
        self,
        unit_of_work: UnitOfWork,
    ) -> None:
        self._unit_of_work = unit_of_work

    async def handle(
        self,
        query: ListAssessmentsQuery,
    ) -> list[ListAssessmentResponseDTO]:
        """
        Retrieve assessments.
        """

        async with self._unit_of_work:
            assessments = await self._unit_of_work.assessment_repository.list(
                page=query.page,
                page_size=query.page_size,
                discovery_id=query.discovery_id,
            )

        return [
            AssessmentMapper.to_list_response(
                assessment,
            )
            for assessment in assessments
        ]
