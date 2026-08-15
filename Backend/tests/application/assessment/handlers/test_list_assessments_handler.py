"""
List Assessment handler.
"""

from __future__ import annotations

from app.application.assessment.assessment_mapper import (
    AssessmentMapper,
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
        page: int = 1,
        page_size: int = 10,
        discovery_id: str | None = None,
    ) -> list[ListAssessmentResponseDTO]:
        """
        Retrieve a list of assessments.
        """

        async with self._unit_of_work:
            assessments = await self._unit_of_work.assessment_repository.list(
                page=page,
                page_size=page_size,
                discovery_id=discovery_id,
            )

        return [
            AssessmentMapper.to_list_response(
                assessment,
            )
            for assessment in assessments
        ]
