"""
Tests for ExecuteAIRequestCommand.
"""

import pytest
from pydantic import ValidationError

from app.application.ai.commands.execute_ai_request import (
    ExecuteAIRequestCommand,
)


# ==========================================================
# Happy Path
# ==========================================================

def test_create_valid_command() -> None:
    """
    Command should be created successfully.
    """

    command = ExecuteAIRequestCommand(
        provider="gemini",
        model="gemini-2.5-pro",
        prompt="Hello AI",
        temperature=0.7,
        max_tokens=1024,
    )

    assert command.provider == "gemini"
    assert command.model == "gemini-2.5-pro"
    assert command.prompt == "Hello AI"
    assert command.temperature == 0.7
    assert command.max_tokens == 1024


# ==========================================================
# Provider
# ==========================================================

def test_provider_is_required() -> None:
    """
    Provider cannot be empty.
    """

    with pytest.raises(ValidationError):

        ExecuteAIRequestCommand(
            provider="",
            model="gemini",
            prompt="Hello",
        )


def test_provider_min_length() -> None:
    """
    Provider must satisfy minimum length.
    """

    with pytest.raises(ValidationError):

        ExecuteAIRequestCommand(
            provider="A",
            model="gemini",
            prompt="Hello",
        )


# ==========================================================
# Model
# ==========================================================

def test_model_is_required() -> None:
    """
    Model cannot be empty.
    """

    with pytest.raises(ValidationError):

        ExecuteAIRequestCommand(
            provider="gemini",
            model="",
            prompt="Hello",
        )


# ==========================================================
# Prompt
# ==========================================================

def test_prompt_is_required() -> None:
    """
    Prompt cannot be empty.
    """

    with pytest.raises(ValidationError):

        ExecuteAIRequestCommand(
            provider="gemini",
            model="gemini-pro",
            prompt="",
        )


# ==========================================================
# Temperature
# ==========================================================

def test_temperature_below_zero_should_fail() -> None:
    """
    Temperature cannot be negative.
    """

    with pytest.raises(ValidationError):

        ExecuteAIRequestCommand(
            provider="gemini",
            model="gemini",
            prompt="Hello",
            temperature=-0.1,
        )


def test_temperature_above_two_should_fail() -> None:
    """
    Temperature cannot exceed two.
    """

    with pytest.raises(ValidationError):

        ExecuteAIRequestCommand(
            provider="gemini",
            model="gemini",
            prompt="Hello",
            temperature=2.1,
        )


# ==========================================================
# Max Tokens
# ==========================================================

def test_max_tokens_must_be_positive() -> None:
    """
    Max tokens must be greater than zero.
    """

    with pytest.raises(ValidationError):

        ExecuteAIRequestCommand(
            provider="gemini",
            model="gemini",
            prompt="Hello",
            max_tokens=0,
        )


# ==========================================================
# Configuration
# ==========================================================

def test_command_is_immutable() -> None:
    """
    Command must be immutable.
    """

    command = ExecuteAIRequestCommand(
        provider="gemini",
        model="gemini",
        prompt="Hello",
    )

    with pytest.raises(ValidationError):

        command.provider = "openai"


def test_extra_fields_are_forbidden() -> None:
    """
    Extra fields should not be accepted.
    """

    with pytest.raises(ValidationError):

        ExecuteAIRequestCommand(
            provider="gemini",
            model="gemini",
            prompt="Hello",
            unknown="value",
        )