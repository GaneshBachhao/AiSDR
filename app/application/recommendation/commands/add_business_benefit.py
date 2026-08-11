from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class AddBusinessBenefitCommand:
    """
    Command to add a business benefit to a solution.
    """

    recommendation_id: UUID

    solution_id: UUID

    title: str

    description: str