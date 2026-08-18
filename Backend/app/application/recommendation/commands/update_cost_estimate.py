from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class UpdateCostEstimateCommand:
    """
    Command to update cost estimate for a solution.
    """

    recommendation_id: UUID

    solution_id: UUID

    estimated_cost: float

    currency: str
