"""
Assessment validator.
"""

from __future__ import annotations

from app.application.assessment.assessment_commands import (
    CreateAssessmentCommand,
    UpdateAssessmentCommand,
)
from app.application.common.validation.validation_result import ValidationResult


class AssessmentValidator:
    """Validates Assessment commands."""

    @staticmethod
    def validate_create(command: CreateAssessmentCommand) -> ValidationResult:
        result = ValidationResult()
        if not command.discovery_id.strip():
            result.add_error("discovery_id", "Discovery identifier is required.")
        return result

    @staticmethod
    def validate_update(command: UpdateAssessmentCommand) -> ValidationResult:
        result = ValidationResult()

        if not command.assessment_id.strip():
            result.add_error("assessment_id", "Assessment identifier is required.")

        if command.readiness_score is not None and not 0 <= command.readiness_score <= 100:
            result.add_error(
                "readiness_score",
                "Readiness score must be between 0 and 100.",
            )

        return result
