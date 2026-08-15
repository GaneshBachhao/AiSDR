from __future__ import annotations

from app.application.common.validation.validation_result import (
    ValidationResult,
)
from app.application.recommendation.commands.add_dependency import (
    AddDependencyCommand,
)


class AddDependencyValidator:
    """
    Validator for AddDependencyCommand.
    """

    def validate(
        self,
        command: AddDependencyCommand,
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

        if not command.name.strip():
            result.add_error(
                field="name",
                message="Dependency name is required.",
            )

        if (
            command.description is not None
            and not command.description.strip()
        ):
            result.add_error(
                field="description",
                message="Dependency description cannot be empty.",
            )

        return result