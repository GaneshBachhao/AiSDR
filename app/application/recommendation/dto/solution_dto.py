from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class SolutionDTO:
    """
    Data transfer object representing a recommended solution.
    """

    id: UUID

    title: str

    description: str

    solution_type: str

    priority: str

    expected_roi: float

    estimated_cost: float

    implementation_risk: str