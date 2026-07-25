from __future__ import annotations

from app.application.recommendation.dto.solution_dto import (
    SolutionDTO,
)
from app.domain.recommendation.entities.solution import (
    Solution,
)


class SolutionMapper:
    """
    Maps Solution entities to DTOs.
    """

    @staticmethod
    def to_dto(
        solution: Solution,
    ) -> SolutionDTO:
        return SolutionDTO(
            id=solution.solution_id,
            title=solution.title,
            description=solution.description,
            solution_type=solution.solution_type.name,
            priority=solution.priority.name,
            expected_roi=(
                solution.roi.value
                if solution.roi is not None
                else 0.0
            ),
            estimated_cost=(
                solution.cost_estimate.value
                if solution.cost_estimate is not None
                else 0.0
            ),
            implementation_risk=(
                solution.implementation_risks[0].level
                if solution.implementation_risks
                else ""
            ),
        )