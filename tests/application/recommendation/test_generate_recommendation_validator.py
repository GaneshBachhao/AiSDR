from uuid import uuid4

from app.application.recommendation.commands.generate_recommendation import (
    GenerateRecommendationCommand,
)
from app.application.recommendation.validators.generate_recommendation_validator import (
    GenerateRecommendationValidator,
)


def test_validator_accepts_valid_command():
    validator = GenerateRecommendationValidator()

    command = GenerateRecommendationCommand(
        assessment_id=uuid4(),
    )

    result = validator.validate(command)

    assert result.is_valid


def test_validator_requires_assessment_id():
    validator = GenerateRecommendationValidator()

    command = GenerateRecommendationCommand.model_construct(
        assessment_id=None,
    )

    result = validator.validate(command)

    assert result.has_error("assessment_id")