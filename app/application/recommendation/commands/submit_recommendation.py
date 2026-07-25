from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class SubmitRecommendationCommand:
    """
    Command to submit a recommendation for review.
    """

    recommendation_id: UUID