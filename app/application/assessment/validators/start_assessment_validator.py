from __future__ import annotations

from app.application.assessment.commands.start_assessment import (
    StartAssessmentCommand,
)
from app.application.common.validation.validation_result import (
    ValidationResult,
)


class StartAssessmentValidator:
    """
    Validates StartAssessmentCommand.

    This validator performs only application-level validation.
    Business rules belong in the domain layer.
    """

    def validate(
        self,
        command: StartAssessmentCommand,
    ) -> ValidationResult:
        """
        Validate the incoming command.
        """

        result = ValidationResult()

        if command.discovery_session_id.int == 0:
            result.add_error(
                "discovery_session_id",
                "Discovery session ID is required.",
            )

        if (
            command.summary is not None
            and not command.summary.strip()
        ):
            result.add_error(
                "summary",
                "Summary cannot be empty.",
            )

        return result