# app/application/assessment/mappers/finding_mapper.py

from __future__ import annotations

from app.application.assessment.dto.finding_dto import (
    FindingDTO,
)
from app.domain.assessment.entities.finding import (
    Finding,
)


class FindingMapper:
    """
    Maps Finding domain entities to application DTOs.
    """

    @staticmethod
    def to_dto(
        finding: Finding,
    ) -> FindingDTO:
        """
        Convert Finding entity into FindingDTO.
        """

        return FindingDTO(
            finding_id=finding.finding_id,
            title=finding.title,
            description=finding.description,
            finding_type=finding.finding_type.name,
            severity=finding.severity,
            recommendation_hint=finding.recommendation_hint,
            evidence_count=len(finding.evidence),
        )