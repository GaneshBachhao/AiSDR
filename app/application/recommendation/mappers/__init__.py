from app.application.recommendation.dto.recommendation_dto import (
    RecommendationDTO,
)


class SolutionMapper:
    """
    Maps solution related objects.
    """

    @staticmethod
    def to_dto(
        recommendation,
    ) -> RecommendationDTO:

        return RecommendationDTO(
            id=recommendation.id.value,
            assessment_id=(
                recommendation.assessment_id.value
                if recommendation.assessment_id
                else None
            ),
            discovery_id=(
                recommendation.discovery_id.value
                if recommendation.discovery_id
                else None
            ),
            status=recommendation.status.value,
            summary=recommendation.summary,
            solutions=recommendation.solutions,
            business_benefits=recommendation.business_benefits,
            dependencies=recommendation.dependencies,
            implementation_risks=recommendation.implementation_risks,
            roadmap_phases=recommendation.roadmap_phases,
            cost_estimate=recommendation.cost_estimate,
            roi=recommendation.roi,
            created_at=recommendation.created_at,
            updated_at=recommendation.updated_at,
        )