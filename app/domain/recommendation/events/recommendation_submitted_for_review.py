from domain.shared.base import DomainEvent

from ..value_objects.recommendation_id import RecommendationId


class RecommendationSubmittedForReview(DomainEvent):
    """
    Raised when a recommendation is submitted for review.
    """

    def __init__(
        self,
        recommendation_id: RecommendationId,
    ) -> None:
        super().__init__()
        self.recommendation_id = recommendation_id