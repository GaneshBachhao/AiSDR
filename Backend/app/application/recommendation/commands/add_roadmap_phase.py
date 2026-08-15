from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class AddRoadmapPhaseCommand:
    """
    Command to add a roadmap phase to a recommendation.
    """

    recommendation_id: UUID

    name: str

    description: str

    sequence: int