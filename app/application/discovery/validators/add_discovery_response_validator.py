from __future__ import annotations

from app.application.common.validation.validation_result import (
    ValidationResult,
)

from app.application.discovery.commands.add_discovery_response import (
    AddDiscoveryResponseCommand,
)


class AddDiscoveryResponseValidator:
    """
    Validates AddDiscoveryResponseCommand.
    """

    def validate(
        self,
        command: AddDiscoveryResponseCommand,
    ) -> ValidationResult:

        result = ValidationResult()

        if not command.question_id.strip():
            result.add_error(
                "question_id",
                "Question id is required.",
            )

        if not command.question.strip():
            result.add_error(
                "question",
                "Question is required.",
            )

        if not command.answer.strip():
            result.add_error(
                "answer",
                "Answer is required.",
            )

        if not 0.0 <= command.confidence <= 1.0:
            result.add_error(
                "confidence",
                "Confidence must be between 0 and 1.",
            )

        return result