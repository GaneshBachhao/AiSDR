from app.domain.shared.base import DomainEvent

from app.domain.recommendation.value_objects.recommendation_id import RecommendationId


class RecommendationApproved(DomainEvent):
    """
    Raised when a recommendation is approved.
    """

    def __init__(self, recommendation_id: RecommendationId):
        super().__init__()
        self.recommendation_id = recommendation_id