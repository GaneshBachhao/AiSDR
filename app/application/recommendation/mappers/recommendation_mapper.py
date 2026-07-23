"""
Recommendation Mapper

Maps between Application commands, Domain aggregates,
and Application DTOs.
"""

from __future__ import annotations

from app.application.recommendation.commands.generate_recommendation import (
    GenerateRecommendationCommand,
)
from app.application.recommendation.dto.recommendation_dto import (
    RecommendationDTO,
    RoadmapPhaseDTO,
    SolutionDTO,
)
from app.domain.assessment.identifiers.assessment_id import (
    AssessmentId,
)
from app.domain.recommendation.entities.recommendation import (
    Recommendation,
)


class RecommendationMapper:
    """
    Mapper for the Recommendation module.
    """

    @staticmethod
    def command_to_assessment_id(
        command: GenerateRecommendationCommand,
    ) -> AssessmentId:
        """
        Convert command into AssessmentId.
        """

        return AssessmentId(
            command.assessment_id,
        )

    @staticmethod
    def domain_to_dto(
        recommendation: Recommendation,
    ) -> RecommendationDTO:
        """
        Convert Recommendation aggregate into DTO.
        """

        return RecommendationDTO(
            id=recommendation.id.value,
            assessment_id=recommendation.assessment_id.value,
            status=recommendation.status.value,
            executive_summary=recommendation.executive_summary,
            solutions=[
                SolutionDTO(
                    title=solution.title,
                    description=solution.description,
                    solution_type=solution.solution_type.value,
                    priority=solution.priority.value,
                )
                for solution in recommendation.solutions
            ],
            roadmap_phases=[
                RoadmapPhaseDTO(
                    name=phase.name,
                    description=phase.description,
                    order=phase.order,
                )
                for phase in recommendation.roadmap_phases
            ],
        )