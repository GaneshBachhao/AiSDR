from typing import List

from sqlalchemy.orm import Session

from app.recommendation.models.recommendation import Recommendation


class RecommendationRepository:
    """
    Handles persistence of AI recommendations.
    """

    def create(
        self,
        db: Session,
        recommendation: Recommendation,
    ) -> Recommendation:

        db.add(recommendation)

        db.commit()

        db.refresh(recommendation)

        return recommendation

    def create_many(
        self,
        db: Session,
        recommendations: List[Recommendation],
    ) -> List[Recommendation]:

        db.add_all(recommendations)

        db.commit()

        for recommendation in recommendations:
            db.refresh(recommendation)

        return recommendations

    def get_by_research(
        self,
        db: Session,
        lead_research_id: int,
    ) -> List[Recommendation]:

        return (
            db.query(Recommendation)
            .filter(
                Recommendation.lead_research_id
                == lead_research_id
            )
            .order_by(
                Recommendation.implementation_order.asc()
            )
            .all()
        )