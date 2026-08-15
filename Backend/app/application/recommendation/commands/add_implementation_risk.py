from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class AddImplementationRiskCommand:
    """
    Command to add an implementation risk
    to a solution.
    """

    recommendation_id: UUID

    solution_id: UUID

    title: str

    description: str

    mitigation: str | None = None