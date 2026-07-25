from __future__ import annotations

from app.application.assessment.commands.add_finding import (
    AddFindingCommand,
)
from app.application.common.validation.validation_result import (
    ValidationResult,
)


class AddFindingValidator:
    """
    Validates AddFindingCommand.
    """

    def validate(
        self,
        command: AddFindingCommand,
    ) -> ValidationResult:

        result = ValidationResult()

        if command.assessment_id.int == 0:
            result.add_error(
                "assessment_id",
                "Assessment ID is required.",
            )

        if not command.title.strip():
            result.add_error(
                "title",
                "Title is required.",
            )

        if not command.description.strip():
            result.add_error(
                "description",
                "Description is required.",
            )

        if not command.finding_type.strip():
            result.add_error(
                "finding_type",
                "Finding type is required.",
            )

        if not 1 <= command.severity <= 5:
            result.add_error(
                "severity",
                "Severity must be between 1 and 5.",
            )

        return result