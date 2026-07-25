from __future__ import annotations

from app.application.common.validation.validation_result import (
    ValidationResult,
)
from app.application.recommendation.commands.submit_recommendation import (
    SubmitRecommendationCommand,
)


class SubmitRecommendationValidator:
    """
    Validator for SubmitRecommendationCommand.
    """

    def validate(
        self,
        command: SubmitRecommendationCommand,
    ) -> ValidationResult:

        result = ValidationResult()

        if command.recommendation_id is None:
            result.add_error(
                field="recommendation_id",
                message="Recommendation ID is required.",
            )

        return result