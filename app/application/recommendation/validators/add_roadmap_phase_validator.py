from __future__ import annotations

from app.application.common.validation.validation_result import (
    ValidationResult,
)
from app.application.recommendation.commands.add_roadmap_phase import (
    AddRoadmapPhaseCommand,
)


class AddRoadmapPhaseValidator:
    """
    Validator for AddRoadmapPhaseCommand.
    """

    def validate(
        self,
        command: AddRoadmapPhaseCommand,
    ) -> ValidationResult:

        result = ValidationResult()

        if command.recommendation_id is None:
            result.add_error(
                field="recommendation_id",
                message="Recommendation ID is required.",
            )

        if not command.name.strip():
            result.add_error(
                field="name",
                message="Roadmap phase name is required.",
            )

        if not command.description.strip():
            result.add_error(
                field="description",
                message="Roadmap phase description is required.",
            )

        if command.sequence < 1:
            result.add_error(
                field="sequence",
                message="Sequence must be greater than zero.",
            )

        return result