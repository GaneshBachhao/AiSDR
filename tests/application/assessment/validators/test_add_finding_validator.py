from uuid import uuid4

from app.application.assessment.commands.add_finding import (
    AddFindingCommand,
)
from app.application.assessment.validators.add_finding_validator import (
    AddFindingValidator,
)


def test_validator_accepts_valid_command():

    validator = AddFindingValidator()

    command = AddFindingCommand(
        assessment_id=uuid4(),
        title="Manual sales process",
        description="Sales team performs repetitive manual work.",
        finding_type="OPPORTUNITY",
        severity=3,
        recommendation_hint="Introduce AI automation.",
    )

    result = validator.validate(command)

    assert result.is_valid


def test_validator_requires_title():

    validator = AddFindingValidator()

    command = AddFindingCommand(
        assessment_id=uuid4(),
        title="",
        description="Description",
        finding_type="RISK",
        severity=3,
    )

    result = validator.validate(command)

    assert not result.is_valid
    assert result.errors


def test_validator_requires_description():

    validator = AddFindingValidator()

    command = AddFindingCommand(
        assessment_id=uuid4(),
        title="Risk",
        description="",
        finding_type="RISK",
        severity=3,
    )

    result = validator.validate(command)

    assert not result.is_valid


def test_validator_rejects_invalid_severity():

    validator = AddFindingValidator()

    command = AddFindingCommand(
        assessment_id=uuid4(),
        title="Risk",
        description="Description",
        finding_type="RISK",
        severity=7,
    )

    result = validator.validate(command)

    assert not result.is_valid