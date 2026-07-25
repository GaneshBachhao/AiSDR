from __future__ import annotations

from app.application.assessment.dto.assessment_dto import (
    AssessmentDTO,
)
from app.domain.assessment.entities.assessment import (
    Assessment,
)


class AssessmentMapper:
    """
    Maps Assessment domain entities to application DTOs.
    """

    @staticmethod
    def to_dto(
        assessment: Assessment,
    ) -> AssessmentDTO:
        """
        Convert Assessment aggregate into AssessmentDTO.
        """

        return AssessmentDTO(
            id=assessment.id.value,
            discovery_session_id=assessment.discovery_session_id.value,
            status=assessment.status.name,
            score=assessment.score.overall_score,
            maturity_level=assessment.maturity_level.name,
            summary=assessment.summary,
            started_at=assessment.started_at,
            completed_at=assessment.completed_at,
            findings_count=len(
                assessment.findings,
            ),
            opportunities_count=len(
                assessment.opportunities,
            ),
        )