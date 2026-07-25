from __future__ import annotations

from app.application.common.validation.validation_result import (
    ValidationResult,
)
from app.application.recommendation.commands.approve_recommendation import (
    ApproveRecommendationCommand,
)


class ApproveRecommendationValidator:
    """
    Validator for ApproveRecommendationCommand.
    """

    def validate(
        self,
        command: ApproveRecommendationCommand,
    ) -> ValidationResult:

        result = ValidationResult()

        if command.recommendation_id is None:
            result.add_error(
                field="recommendation_id",
                message="Recommendation ID is required.",
            )

        return result