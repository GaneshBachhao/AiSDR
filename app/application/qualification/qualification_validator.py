"""
Qualification application validation.
"""

from __future__ import annotations

from uuid import UUID

from app.application.common.validation.validation_result import ValidationResult
from app.application.qualification.qualification_commands import (
    CreateQualificationCommand,
    UpdateQualificationCommand,
)
from app.domain.qualification.enums.qualification_status import QualificationStatus


class QualificationValidator:
    """Validate Qualification commands at the application boundary."""

    @staticmethod
    def _is_uuid(value: str) -> bool:
        try:
            UUID(value.strip())
        except (TypeError, ValueError, AttributeError):
            return False
        return True

    @staticmethod
    def normalize_status(value: str) -> QualificationStatus | None:
        """Resolve a persisted/API status using enum values or names."""
        if not value or not value.strip():
            return None

        normalized = value.strip()
        try:
            return QualificationStatus(normalized)
        except ValueError:
            key = normalized.upper().replace(" ", "_").replace("-", "_")
            try:
                return QualificationStatus[key]
            except KeyError:
                return None

    @classmethod
    def validate_create(
        cls,
        command: CreateQualificationCommand,
    ) -> ValidationResult:
        result = ValidationResult()

        if not command.lead_id.strip():
            result.add_error("lead_id", "Lead identifier is required.")
        elif not cls._is_uuid(command.lead_id):
            result.add_error("lead_id", "Invalid lead id.")

        if not command.assessment_id.strip():
            result.add_error("assessment_id", "Assessment identifier is required.")
        elif not cls._is_uuid(command.assessment_id):
            result.add_error("assessment_id", "Invalid assessment id.")

        if command.status is not None and cls.normalize_status(command.status) is None:
            result.add_error("status", "Invalid qualification status.")

        if command.score is not None and not 0 <= command.score <= 100:
            result.add_error(
                "score",
                "Qualification score must be between 0 and 100.",
            )

        return result

    @classmethod
    def validate_update(
        cls,
        command: UpdateQualificationCommand,
    ) -> ValidationResult:
        result = ValidationResult()

        if not command.qualification_id.strip():
            result.add_error(
                "qualification_id",
                "Qualification identifier is required.",
            )
        elif not cls._is_uuid(command.qualification_id):
            result.add_error("qualification_id", "Invalid qualification id.")

        if command.status is not None and cls.normalize_status(command.status) is None:
            result.add_error("status", "Invalid qualification status.")

        if command.score is not None and not 0 <= command.score <= 100:
            result.add_error(
                "score",
                "Qualification score must be between 0 and 100.",
            )

        return result
