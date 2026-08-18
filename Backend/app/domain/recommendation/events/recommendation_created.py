from app.domain.shared.base import DomainEvent

from ..identifiers.recommendation_id import RecommendationId


class RecommendationCreated(DomainEvent):
    """
    Raised when a recommendation is created.
    """

    def __init__(self, recommendation_id: RecommendationId):
        super().__init__()
        self.recommendation_id = recommendation_id
