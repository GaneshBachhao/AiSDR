"""List Qualification application handler."""

from __future__ import annotations

from app.application.common.exceptions.validation_exception import ValidationException
from app.application.common.interfaces.unit_of_work import UnitOfWork
from app.application.qualification.dto.qualification_response import ListQualificationResponseDTO
from app.application.qualification.qualification_mapper import QualificationMapper
from app.application.qualification.qualification_queries import ListQualificationsQuery
from app.domain.assessment.identifiers.assessment_id import AssessmentId
from app.domain.lead.identifiers.lead_id import LeadId


class ListQualificationHandler:
    """Retrieve paginated Qualifications with optional relationship filters."""

    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self._unit_of_work = unit_of_work

    async def handle(self, query: ListQualificationsQuery) -> list[ListQualificationResponseDTO]:
        if query.page < 1 or query.page_size < 1:
            raise ValidationException(
                message="Invalid pagination parameters.",
                details={"page": query.page, "page_size": query.page_size},
            )

        try:
            lead_id = LeadId(query.lead_id) if query.lead_id else None
            assessment_id = AssessmentId(query.assessment_id) if query.assessment_id else None
        except (TypeError, ValueError) as exc:
            raise ValidationException(
                message="Invalid qualification filter.",
                details={
                    "lead_id": query.lead_id,
                    "assessment_id": query.assessment_id,
                },
            ) from exc

        async with self._unit_of_work:
            qualifications = await self._unit_of_work.qualification_repository.list(
                page=query.page,
                page_size=query.page_size,
                lead_id=lead_id,
                assessment_id=assessment_id,
            )

        return [QualificationMapper.to_list_response(qualification) for qualification in qualifications]
