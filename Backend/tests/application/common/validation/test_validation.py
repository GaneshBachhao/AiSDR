# tests/application/common/validation/test_validation.py

from __future__ import annotations

import pytest

from app.application.common.validation import (
    ValidationResult,
    Validator,
)


class SampleRequest:
    """
    Test request object.
    """

    def __init__(
        self,
        value: str,
    ) -> None:
        self.value = value


class SampleValidator(
    Validator[SampleRequest],
):
    """
    Test validator.
    """

    async def validate(
        self,
        request: SampleRequest,
    ) -> ValidationResult:

        result = ValidationResult()

        if not request.value:
            result.add_error(
                field="value",
                message="Value is required.",
            )

        return result


def test_validation_result_defaults_valid() -> None:
    result = ValidationResult()

    assert result.is_valid is True
    assert result.errors == []


def test_validation_result_adds_error() -> None:
    result = ValidationResult()

    result.add_error(
        field="name",
        message="Name is required.",
    )

    assert result.is_valid is False
    assert len(result.errors) == 1
    assert result.errors[0].field == "name"


@pytest.mark.asyncio
async def test_validator_returns_valid_result() -> None:
    validator = SampleValidator()

    result = await validator.validate(
        SampleRequest(
            value="Pamacore",
        ),
    )

    assert result.is_valid is True


@pytest.mark.asyncio
async def test_validator_returns_invalid_result() -> None:
    validator = SampleValidator()

    result = await validator.validate(
        SampleRequest(
            value="",
        ),
    )

    assert result.is_valid is False
    assert result.errors[0].message == "Value is required."
