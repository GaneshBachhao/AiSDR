from __future__ import annotations

from app.application.common.validation.validation_result import (
    ValidationResult,
)
from app.application.recommendation.commands.update_cost_estimate import (
    UpdateCostEstimateCommand,
)


class UpdateCostEstimateValidator:
    """
    Validator for UpdateCostEstimateCommand.
    """

    def validate(
        self,
        command: UpdateCostEstimateCommand,
    ) -> ValidationResult:

        result = ValidationResult()

        if command.recommendation_id is None:
            result.add_error(
                field="recommendation_id",
                message="Recommendation ID is required.",
            )

        if command.solution_id is None:
            result.add_error(
                field="solution_id",
                message="Solution ID is required.",
            )

        if command.estimated_cost < 0:
            result.add_error(
                field="estimated_cost",
                message="Estimated cost cannot be negative.",
            )

        if not command.currency.strip():
            result.add_error(
                field="currency",
                message="Currency is required.",
            )

        return result