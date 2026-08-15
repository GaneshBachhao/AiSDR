from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class ApproveRecommendationCommand:
    """
    Command to approve a recommendation.
    """

    recommendation_id: UUID