from __future__ import annotations

from app.application.assessment.commands.update_assessment_score import (
    UpdateAssessmentScoreCommand,
)
from app.application.common.validation.validation_result import (
    ValidationResult,
)


class UpdateAssessmentScoreValidator:
    """
    Validates UpdateAssessmentScoreCommand.
    """

    def validate(
        self,
        command: UpdateAssessmentScoreCommand,
    ) -> ValidationResult:

        result = ValidationResult()

        if command.assessment_id.int == 0:
            result.add_error(
                "assessment_id",
                "Assessment ID is required.",
            )

        scores = (
            command.overall_score,
            command.strategy_score,
            command.process_score,
            command.technology_score,
            command.data_score,
            command.people_score,
        )

        for score in scores:
            if not 0 <= score <= 100:
                result.add_error(
                    "score",
                    "Scores must be between 0 and 100.",
                )
                break

        return result