from app.application.common.operation_result import (
    OperationResult,
)


class SubmitRecommendationValidator:
    """
    Validates submission request.
    """

    def validate(
        self,
        command,
    ):

        result = OperationResult(success=True)

        if not command.recommendation_id:
            result.add_error("Recommendation id is required.")

        return result
