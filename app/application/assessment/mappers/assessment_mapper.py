"""
Assessment Mapper.
"""

from __future__ import annotations

from app.application.assessment.dto.assessment_dto import (
    AssessmentDTO,
)
from app.domain.assessment.entities.assessment import (
    Assessment,
)


class AssessmentMapper:
    """
    Maps Assessment aggregate to DTO.
    """

    @staticmethod
    def to_dto(
        assessment: Assessment,
    ) -> AssessmentDTO:

        return AssessmentDTO(
            id=assessment.id.value,
            discovery_session_id=assessment.discovery_session_id.value,
            status=assessment.status.name,
            overall_score=assessment.score.overall_score,
            maturity_level=assessment.maturity_level.name,
            summary=assessment.summary,
        )