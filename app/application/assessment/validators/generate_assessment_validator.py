"""
Generate Assessment Validator.
"""

from __future__ import annotations

from app.application.assessment.commands.generate_assessment import (
    GenerateAssessmentCommand,
)
from app.application.common.validation.validation_result import (
    ValidationResult,
)


class GenerateAssessmentValidator:
    """
    Application validator for GenerateAssessmentCommand.
    """

    def validate(
        self,
        command: GenerateAssessmentCommand,
    ) -> ValidationResult:

        result = ValidationResult()

        if command.discovery_session_id is None:
            result.add_error(
                "discovery_session_id",
                "Discovery session id is required.",
            )

        return result