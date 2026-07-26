from __future__ import annotations

from app.application.recommendation.dto.recommendation_dto import (
    RecommendationDTO,
)

from app.domain.assessment.identifiers.assessment_id import (
    AssessmentId,
)


class RecommendationMapper:
    """
    Backward-compatible mapper.

    Supports both:

        mapper.domain_to_dto(...)
        mapper.to_dto(...)

    and

        RecommendationMapper.command_to_assessment_id(...)
    """

    @staticmethod
    def command_to_assessment_id(command) -> AssessmentId:
        """
        Convert command -> AssessmentId.
        """
        return AssessmentId(command.assessment_id)

    @staticmethod
    def domain_to_dto(
        recommendation,
    ) -> RecommendationDTO:

        return RecommendationDTO(
            id=recommendation.id.value,
            assessment_id=recommendation.assessment_id.value,
            status=recommendation.status.value,
            title=None,
            summary=recommendation.executive_summary,
            recommendation_text=None,
            business_benefits=[],
            solutions=[
                solution.title
                for solution in recommendation.solutions
            ],
            dependencies=[],
            implementation_risks=[],
            roadmap_phases=[
                getattr(
                    phase,
                    "title",
                    getattr(
                        phase,
                        "phase_name",
                        "",
                    ),
                )
                for phase in recommendation.roadmap_phases
            ],
            cost_estimate=None,
            roi_percentage=None,
            created_at=recommendation.created_at,
            updated_at=recommendation.updated_at,
        )

    def to_dto(
        self,
        recommendation,
    ) -> RecommendationDTO:
        """
        Alias used by older handlers.
        """
        return self.domain_to_dto(
            recommendation,
        )