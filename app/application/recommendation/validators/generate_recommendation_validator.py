from __future__ import annotations

from app.application.common.validation.validation_result import (
    ValidationResult,
)
from app.application.recommendation.commands.generate_recommendation import (
    GenerateRecommendationCommand,
)


class GenerateRecommendationValidator:
    """
    Validates GenerateRecommendationCommand.

    Performs only application-level validation.
    Business rules belong to the domain layer.
    """

    def validate(
        self,
        command: GenerateRecommendationCommand,
    ) -> ValidationResult:
        """
        Validate the incoming command.
        """
        result = ValidationResult()

        if command.assessment_id is None:
            result.add_error(
                "assessment_id",
                "Assessment identifier is required.",
            )

        return result