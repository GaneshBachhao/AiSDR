from __future__ import annotations

from app.application.recommendation.dto.roadmap_phase_dto import (
    RoadmapPhaseDTO,
)
from app.domain.recommendation.entities.roadmap_phase import (
    RoadmapPhase,
)


class RoadmapPhaseMapper:
    """
    Maps RoadmapPhase entities to DTOs.
    """

    @staticmethod
    def to_dto(
        roadmap_phase: RoadmapPhase,
    ) -> RoadmapPhaseDTO:
        return RoadmapPhaseDTO(
            name=roadmap_phase.name,
            priority=roadmap_phase.priority.name,
            duration=roadmap_phase.duration,
            solution_count=len(
                roadmap_phase.solutions,
            ),
        )