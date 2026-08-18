from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class UpdateROICommand:
    """
    Command to update ROI information for a solution.
    """

    recommendation_id: UUID

    solution_id: UUID

    expected_return: float

    investment_cost: float
