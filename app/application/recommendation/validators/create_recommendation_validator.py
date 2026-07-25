from __future__ import annotations

from app.application.common.validation.validation_result import (
    ValidationResult,
)
from app.application.recommendation.commands.create_recommendation import (
    CreateRecommendationCommand,
)


class CreateRecommendationValidator:
    """
    Validator for CreateRecommendationCommand.
    """

    def validate(
        self,
        command: CreateRecommendationCommand,
    ) -> ValidationResult:

        result = ValidationResult()

        if command.assessment_id is None:
            result.add_error(
                field="assessment_id",
                message="Assessment ID is required.",
            )

        return result