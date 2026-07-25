from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RoadmapPhaseDTO:
    """
    Data transfer object representing a roadmap phase.
    """

    name: str

    priority: str

    duration: str

    solution_count: int