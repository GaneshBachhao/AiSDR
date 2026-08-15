from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class RoadmapPhase:
    """
    Represents a recommended implementation phase.

    A roadmap phase defines the recommended sequence,
    estimated duration, and expected deliverables for
    implementing the proposed AI solution.

    This entity belongs to the Recommendation domain and
    represents planning only. Actual execution and progress
    tracking are managed by the Project/Workflow domain.
    """

    phase_name: str

    sequence: int

    description: str

    estimated_duration: str

    deliverables: list[str] = field(default_factory=list)

    roadmap_phase_id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        """
        Validate business invariants.
        """
        if not self.phase_name.strip():
            raise ValueError(
                "Phase name cannot be empty."
            )

        if not self.description.strip():
            raise ValueError(
                "Description cannot be empty."
            )

        if not self.estimated_duration.strip():
            raise ValueError(
                "Estimated duration cannot be empty."
            )

        if self.sequence < 1:
            raise ValueError(
                "Roadmap phase sequence must be greater than zero."
            )

    def add_deliverable(
        self,
        deliverable: str,
    ) -> None:
        """
        Add a deliverable to this roadmap phase.
        """
        deliverable = deliverable.strip()

        if not deliverable:
            raise ValueError(
                "Deliverable cannot be empty."
            )

        if deliverable not in self.deliverables:
            self.deliverables.append(deliverable)

    def remove_deliverable(
        self,
        deliverable: str,
    ) -> None:
        """
        Remove a deliverable from this roadmap phase.
        """
        if deliverable in self.deliverables:
            self.deliverables.remove(deliverable)