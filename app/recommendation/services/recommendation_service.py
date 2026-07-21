from app.recommendation.schemas.recommendation_schema import (
    RecommendationItem,
    RecommendationResponse,
)

from sqlalchemy.orm import Session

from app.recommendation.models.recommendation import Recommendation
from app.recommendation.repositories.recommendation_repository import  RecommendationRepository


class RecommendationService:
    """
    Converts enriched research into structured recommendations.
    """


    def __init__(self):
        self.repository = RecommendationRepository()


    def save(
        self,
        db: Session,
        lead_research_id: int,
        recommendation_response: RecommendationResponse,
    ) -> list[Recommendation]:
        """
        Persist generated recommendations.
        """

        recommendations = []

        for order, item in enumerate(
            recommendation_response.recommendations,
            start=1,
        ):

            recommendations.append(

                Recommendation(

                    lead_research_id=lead_research_id,

                    service_id=item.service_id,

                    service_name=item.service_name,

                    category=item.category,

                    priority=item.priority,

                    difficulty=item.difficulty,

                    roi=item.roi,

                    implementation_order=order,
                )
            )

        return self.repository.create_many(
            db,
            recommendations,
        )


    def generate(
        self,
        enriched_research: dict,
    ) -> RecommendationResponse:

        recommendations = []

        for service in enriched_research.get(
            "catalog_services",
            [],
        ):

            recommendations.append(

                RecommendationItem(

                    service_id=service["id"],

                    service_name=service["name"],

                    category=service["category"],

                    priority=service["priority"],

                    difficulty=service["difficulty"],

                    roi=service["roi"],

                    target_personas=service.get(
                        "target_personas",
                        [],
                    ),

                    deliverables=service.get(
                        "deliverables",
                        [],
                    ),

                    estimated_duration_weeks=service.get(
                        "estimated_duration_weeks",
                        0,
                    ),
                )

            )

        return RecommendationResponse(

            matched_sector=enriched_research.get(
                "matched_sector",
                "Unknown",
            ),

            sector_confidence=enriched_research.get(
                "sector_confidence",
                0.0,
            ),

            recommendations=recommendations,

            generic_ai_opportunities=enriched_research.get(
                "generic_ai_opportunities",
                [],
            ),
        )