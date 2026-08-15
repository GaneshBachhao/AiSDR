from __future__ import annotations

from app.application.common.validation.validation_result import (
    ValidationResult,
)
from app.application.recommendation.commands.update_roi import (
    UpdateROICommand,
)


class UpdateROIValidator:
    """
    Validator for UpdateROICommand.
    """

    def validate(
        self,
        command: UpdateROICommand,
    ) -> ValidationResult:

        result = ValidationResult()

        if command.recommendation_id is None:
            result.add_error(
                field="recommendation_id",
                message="Recommendation ID is required.",
            )

        if command.expected_return < 0:
            result.add_error(
                field="expected_return",
                message="Expected return cannot be negative.",
            )

        if command.investment_cost < 0:
            result.add_error(
                field="investment_cost",
                message="Investment cost cannot be negative.",
            )

        if (
            command.investment_cost == 0
            and command.expected_return > 0
        ):
            result.add_error(
                field="investment_cost",
                message="Investment cost must be greater than zero when calculating ROI.",
            )

        return result