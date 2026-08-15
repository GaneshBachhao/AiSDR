"""Recommendation application mapper."""

from __future__ import annotations

from app.application.recommendation.dto.recommendation_dto import (
    RecommendationDTO,
    SolutionSummaryDTO,
)
from app.domain.assessment.identifiers.assessment_id import AssessmentId


class RecommendationMapper:
    """Map application commands and domain aggregates."""

    @staticmethod
    def command_to_assessment_id(command) -> AssessmentId:
        return AssessmentId(command.assessment_id)

    @staticmethod
    def domain_to_dto(recommendation) -> RecommendationDTO:
        return RecommendationDTO(
            id=recommendation.id.value,
            assessment_id=recommendation.assessment_id.value,
            status=recommendation.status.value,
            executive_summary=recommendation.executive_summary,
            submitted_at=recommendation.submitted_at,
            approved_at=recommendation.approved_at,
            solutions=[
                SolutionSummaryDTO(
                    solution_id=solution.solution_id,
                    title=solution.title,
                    description=solution.description,
                    solution_type=solution.solution_type.value,
                    priority=solution.priority.value,
                    is_existing_offering=solution.is_existing_offering,
                )
                for solution in recommendation.solutions
            ],
            roadmap_phases=[
                getattr(phase, "title", getattr(phase, "phase_name", ""))
                for phase in recommendation.roadmap_phases
            ],
            created_at=recommendation.created_at,
            updated_at=recommendation.updated_at,
        )
