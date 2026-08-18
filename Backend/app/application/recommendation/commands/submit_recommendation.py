from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class SubmitRecommendationCommand:
    """
    Command to submit a recommendation.
    """

    recommendation_id: UUID
