from uuid import uuid4

from app.application.assessment.commands.update_assessment_score import (
    UpdateAssessmentScoreCommand,
)
from app.application.assessment.validators.update_assessment_score_validator import (
    UpdateAssessmentScoreValidator,
)


def test_validator_accepts_valid_command():

    validator = UpdateAssessmentScoreValidator()

    command = UpdateAssessmentScoreCommand(
        assessment_id=uuid4(),
        overall_score=82,
        strategy_score=80,
        process_score=85,
        technology_score=78,
        data_score=83,
        people_score=84,
    )

    result = validator.validate(command)

    assert result.is_valid


def test_validator_rejects_invalid_score():

    validator = UpdateAssessmentScoreValidator()

    command = UpdateAssessmentScoreCommand(
        assessment_id=uuid4(),
        overall_score=120,
    )

    result = validator.validate(command)

    assert not result.is_valid