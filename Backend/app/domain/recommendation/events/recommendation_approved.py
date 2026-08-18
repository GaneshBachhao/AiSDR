from app.domain.recommendation.identifiers.recommendation_id import RecommendationId
from app.domain.shared.base import DomainEvent


class RecommendationApproved(DomainEvent):
    """
    Raised when a recommendation is approved.
    """

    def __init__(self, recommendation_id: RecommendationId):
        super().__init__()
        self.recommendation_id = recommendation_id
