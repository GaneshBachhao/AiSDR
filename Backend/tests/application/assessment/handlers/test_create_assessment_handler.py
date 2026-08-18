"""
Tests for CreateAssessmentHandler.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy.exc import IntegrityError

from app.application.assessment.assessment_commands import (
    CreateAssessmentCommand,
)
from app.application.assessment.handlers.create_assessment_handler import (
    CreateAssessmentHandler,
)
from app.application.common.exceptions.conflict_exception import (
    ConflictException,
)


@pytest.fixture
def unit_of_work():

    uow = AsyncMock()

    uow.__aenter__.return_value = uow
    uow.__aexit__.return_value = False

    return uow


@pytest.fixture
def handler(
    unit_of_work,
):

    return CreateAssessmentHandler(
        unit_of_work=unit_of_work,
    )


@pytest.mark.asyncio
async def test_create_assessment_success(
    handler,
    unit_of_work,
):
    """
    Assessment should be created successfully.
    """

    command = CreateAssessmentCommand(
        discovery_id="00000000-0000-0000-0000-000000000001",
    )

    unit_of_work.assessment_repository.get_by_discovery.return_value = None

    with (
        patch(
            "app.application.assessment.handlers.create_assessment_handler.AssessmentValidator.validate_create"
        ) as validator,
        patch(
            "app.application.assessment.handlers.create_assessment_handler.AssessmentMapper.to_create_response"
        ) as mapper,
    ):
        validator.return_value.has_errors.return_value = False

        mapper.return_value = "response"

        result = await handler.handle(command)

    validator.assert_called_once_with(command)

    unit_of_work.assessment_repository.get_by_discovery.assert_awaited_once()

    unit_of_work.assessment_repository.add.assert_awaited_once()

    mapper.assert_called_once()

    assert result == "response"


@pytest.mark.asyncio
async def test_create_assessment_rejects_a_duplicate_discovery_with_conflict(
    handler,
    unit_of_work,
):
    """Regression guard: discovery_id is a unique column (a Discovery can
    have at most one Assessment), but this used to have no pre-check at
    all -- a duplicate create would fall straight through to a raw,
    unformatted IntegrityError/500. It must now raise a clean
    ConflictException instead."""

    command = CreateAssessmentCommand(
        discovery_id="00000000-0000-0000-0000-000000000001",
    )

    unit_of_work.assessment_repository.get_by_discovery.return_value = object()

    with patch(
        "app.application.assessment.handlers.create_assessment_handler.AssessmentValidator.validate_create"
    ) as validator:
        validator.return_value.has_errors.return_value = False

        with pytest.raises(ConflictException):
            await handler.handle(command)

    unit_of_work.assessment_repository.add.assert_not_awaited()


@pytest.mark.asyncio
async def test_create_assessment_maps_a_concurrent_integrity_error_to_conflict(
    handler,
    unit_of_work,
):
    """The pre-check covers the common case; a concurrent duplicate insert
    that slips past it (a race between two requests for the same
    discovery_id) must still surface as a clean ConflictException, not a
    raw IntegrityError."""

    command = CreateAssessmentCommand(
        discovery_id="00000000-0000-0000-0000-000000000001",
    )

    unit_of_work.assessment_repository.get_by_discovery.return_value = None
    unit_of_work.commit.side_effect = IntegrityError("stmt", "params", Exception("UNIQUE constraint failed"))

    with patch(
        "app.application.assessment.handlers.create_assessment_handler.AssessmentValidator.validate_create"
    ) as validator:
        validator.return_value.has_errors.return_value = False

        with pytest.raises(ConflictException):
            await handler.handle(command)


@pytest.mark.asyncio
async def test_create_assessment_validation_failure(
    handler,
):
    """
    Invalid assessment should raise ValueError.
    """

    command = CreateAssessmentCommand(
        discovery_id="",
    )

    with patch(
        "app.application.assessment.handlers.create_assessment_handler.AssessmentValidator.validate_create"
    ) as validator:
        validator.return_value.has_errors.return_value = True

        validator.return_value.error_messages.return_value = "Validation failed."

        with pytest.raises(ValueError):
            await handler.handle(command)
