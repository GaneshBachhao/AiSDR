from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class CreateRecommendationCommand:
    """
    Command to create a recommendation from an assessment.
    """

    assessment_id: UUID