from uuid import uuid4

from app.application.assessment.commands.start_assessment import (
    StartAssessmentCommand,
)
from app.application.assessment.validators.start_assessment_validator import (
    StartAssessmentValidator,
)


def test_validator_accepts_valid_command():

    validator = StartAssessmentValidator()

    command = StartAssessmentCommand(
        discovery_session_id=uuid4(),
        summary="Assessment initiated",
    )

    result = validator.validate(command)

    assert result.is_valid


def test_validator_rejects_blank_summary():

    validator = StartAssessmentValidator()

    command = StartAssessmentCommand(
        discovery_session_id=uuid4(),
        summary="   ",
    )

    result = validator.validate(command)

    assert not result.is_valid
    assert result.errors