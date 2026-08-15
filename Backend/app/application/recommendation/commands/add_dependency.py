from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class AddDependencyCommand:
    """
    Command to add a dependency
    to a recommendation solution.
    """

    recommendation_id: UUID

    solution_id: UUID

    name: str

    description: str | None = None