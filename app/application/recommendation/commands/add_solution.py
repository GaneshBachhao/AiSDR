from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class AddSolutionCommand:
    """
    Command to add a solution to a recommendation.
    """

    recommendation_id: UUID

    title: str

    description: str

    solution_type: str

    priority: str