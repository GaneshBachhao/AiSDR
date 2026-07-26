from app.application.common.operation_result import OperationResult
from app.application.recommendation.commands.create_recommendation import (
    CreateRecommendationCommand,
)


class CreateRecommendationValidator:

    def validate(
        self,
        command: CreateRecommendationCommand,
    ) -> OperationResult:

        result = OperationResult(
            success=True,
        )

        if not command.assessment_id:
            result.add_error(
                "Assessment id is required.",
            )

        return result