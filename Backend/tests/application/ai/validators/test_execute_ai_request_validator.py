"""
Tests for ExecuteAIRequestValidator.
"""

from app.application.ai.commands.execute_ai_request import (
    ExecuteAIRequestCommand,
)
from app.application.ai.validators.execute_ai_request_validator import (
    ExecuteAIRequestValidator,
)


# ==========================================================
# Helpers
# ==========================================================

def create_command() -> ExecuteAIRequestCommand:
    """
    Create a valid command.
    """

    return ExecuteAIRequestCommand(
        provider="gemini",
        model="gemini-2.5-pro",
        prompt="Explain Clean Architecture.",
        temperature=0.7,
        max_tokens=1024,
    )


# ==========================================================
# Happy Path
# ==========================================================

def test_validator_accepts_valid_command() -> None:
    """
    Validator should accept a valid command.
    """

    validator = ExecuteAIRequestValidator()

    result = validator.validate(
        create_command(),
    )

    assert result.is_valid
    assert result.errors == []


# ==========================================================
# Provider
# ==========================================================

def test_validator_rejects_blank_provider() -> None:
    """
    Provider containing only whitespace should fail.
    """

    validator = ExecuteAIRequestValidator()

    command = create_command().model_copy(
        update={
            "provider": "   ",
        }
    )

    result = validator.validate(command)

    assert not result.is_valid
    assert len(result.errors) == 1
    assert result.errors[0].field == "provider"


# ==========================================================
# Model
# ==========================================================

def test_validator_rejects_blank_model() -> None:
    """
    Model containing only whitespace should fail.
    """

    validator = ExecuteAIRequestValidator()

    command = create_command().model_copy(
        update={
            "model": "   ",
        }
    )

    result = validator.validate(command)

    assert not result.is_valid
    assert len(result.errors) == 1
    assert result.errors[0].field == "model"


# ==========================================================
# Prompt
# ==========================================================

def test_validator_rejects_blank_prompt() -> None:
    """
    Prompt containing only whitespace should fail.
    """

    validator = ExecuteAIRequestValidator()

    command = create_command().model_copy(
        update={
            "prompt": "   ",
        }
    )

    result = validator.validate(command)

    assert not result.is_valid
    assert len(result.errors) == 1
    assert result.errors[0].field == "prompt"


# ==========================================================
# Multiple Errors
# ==========================================================

def test_validator_returns_multiple_errors() -> None:
    """
    Validator should collect all validation errors.
    """

    validator = ExecuteAIRequestValidator()

    command = create_command().model_copy(
        update={
            "provider": " ",
            "model": " ",
            "prompt": " ",
        }
    )

    result = validator.validate(command)

    assert not result.is_valid
    assert len(result.errors) == 3

    fields = {
        error.field
        for error in result.errors
    }

    assert fields == {
        "provider",
        "model",
        "prompt",
    }


# ==========================================================
# Validation Messages
# ==========================================================

def test_validator_returns_provider_message() -> None:
    """
    Provider validation message should be correct.
    """

    validator = ExecuteAIRequestValidator()

    command = create_command().model_copy(
        update={
            "provider": " ",
        }
    )

    result = validator.validate(command)

    assert result.errors[0].message == "Provider is required."


def test_validator_returns_model_message() -> None:
    """
    Model validation message should be correct.
    """

    validator = ExecuteAIRequestValidator()

    command = create_command().model_copy(
        update={
            "model": " ",
        }
    )

    result = validator.validate(command)

    assert result.errors[0].message == "Model is required."


def test_validator_returns_prompt_message() -> None:
    """
    Prompt validation message should be correct.
    """

    validator = ExecuteAIRequestValidator()

    command = create_command().model_copy(
        update={
            "prompt": " ",
        }
    )

    result = validator.validate(command)

    assert result.errors[0].message == "Prompt is required."