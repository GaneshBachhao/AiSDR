from __future__ import annotations

from app.application.common.validation.validation_result import (
    ValidationResult,
)
from app.application.recommendation.commands.add_solution import (
    AddSolutionCommand,
)


class AddSolutionValidator:
    """
    Validator for AddSolutionCommand.
    """

    def validate(
        self,
        command: AddSolutionCommand,
    ) -> ValidationResult:

        result = ValidationResult()

        if command.recommendation_id is None:
            result.add_error(
                field="recommendation_id",
                message="Recommendation ID is required.",
            )

        if not command.title.strip():
            result.add_error(
                field="title",
                message="Title is required.",
            )

        if not command.description.strip():
            result.add_error(
                field="description",
                message="Description is required.",
            )

        if not command.solution_type.strip():
            result.add_error(
                field="solution_type",
                message="Solution type is required.",
            )

        if not command.priority.strip():
            result.add_error(
                field="priority",
                message="Priority is required.",
            )

        return result