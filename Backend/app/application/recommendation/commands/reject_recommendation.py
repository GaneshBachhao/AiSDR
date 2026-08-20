from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class RejectRecommendationCommand:
    """
    Command to reject a recommendation.
    """

    recommendation_id: UUID
