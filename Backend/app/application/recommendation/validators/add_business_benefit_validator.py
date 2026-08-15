from __future__ import annotations

from app.application.common.validation.validation_result import (
    ValidationResult,
)
from app.application.recommendation.commands.add_business_benefit import (
    AddBusinessBenefitCommand,
)


class AddBusinessBenefitValidator:
    """
    Validator for AddBusinessBenefitCommand.
    """

    def validate(
        self,
        command: AddBusinessBenefitCommand,
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

        if not command.title.strip():
            result.add_error(
                field="title",
                message="Business benefit title is required.",
            )

        if not command.description.strip():
            result.add_error(
                field="description",
                message="Business benefit description is required.",
            )

        return result