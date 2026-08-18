from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class GetRecommendationByIdQuery:
    """
    Query to retrieve a recommendation by identifier.
    """

    recommendation_id: UUID
