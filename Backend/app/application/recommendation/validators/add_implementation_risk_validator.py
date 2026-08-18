from __future__ import annotations

from app.application.common.validation.validation_result import (
    ValidationResult,
)
from app.application.recommendation.commands.add_implementation_risk import (
    AddImplementationRiskCommand,
)


class AddImplementationRiskValidator:
    """
    Validator for AddImplementationRiskCommand.
    """

    def validate(
        self,
        command: AddImplementationRiskCommand,
    ) -> ValidationResult:

        result = ValidationResult()

        if command.recommendation_id is None:
            result.add_error(
                field="recommendation_id",
                message="Recommendation ID is required.",
            )

        if command.solution_id is None:
            result.add_error(
                field="solution_id",
                message="Solution ID is required.",
            )

        if not command.title.strip():
            result.add_error(
                field="title",
                message="Risk title is required.",
            )

        if not command.description.strip():
            result.add_error(
                field="description",
                message="Risk description is required.",
            )

        if command.mitigation is not None and not command.mitigation.strip():
            result.add_error(
                field="mitigation",
                message="Mitigation cannot be empty.",
            )

        return result
