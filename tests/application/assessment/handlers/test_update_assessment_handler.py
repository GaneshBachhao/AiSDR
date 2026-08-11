"""
Tests for UpdateAssessmentHandler.
"""

from __future__ import annotations

from unittest.mock import AsyncMock
from unittest.mock import Mock
from unittest.mock import patch

import pytest

from app.application.assessment.assessment_commands import (
    UpdateAssessmentCommand,
)
from app.application.assessment.handlers.update_assessment_handler import (
    UpdateAssessmentHandler,
)
from app.application.common.exceptions.not_found_exception import (
    NotFoundException,
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

    return UpdateAssessmentHandler(
        unit_of_work=unit_of_work,
    )


@pytest.mark.asyncio
async def test_update_assessment_success(
    handler,
    unit_of_work,
):
    """
    Assessment should be updated successfully.
    """

    assessment = Mock()

    unit_of_work.assessment_repository.get_by_id.return_value = (
        assessment
    )

    command = UpdateAssessmentCommand(
        assessment_id="00000000-0000-0000-0000-000000000002",
        summary="Updated summary",
        maturity_level="Advanced",
        readiness_score=90,
    )

    with (
        patch(
            "app.application.assessment.handlers.update_assessment_handler.AssessmentValidator.validate_update"
        ) as validator,
        patch(
            "app.application.assessment.handlers.update_assessment_handler.AssessmentMapper.to_update_response"
        ) as mapper,
    ):

        validator.return_value.has_errors.return_value = False

        mapper.return_value = "response"

        result = await handler.handle(command)

    validator.assert_called_once_with(command)

    unit_of_work.assessment_repository.get_by_id.assert_awaited_once()

    assessment.update_maturity.assert_called_once()

    assessment.update_score.assert_called_once()

    unit_of_work.assessment_repository.update.assert_awaited_once_with(
        assessment,
    )

    mapper.assert_called_once_with(assessment)

    assert result == "response"


@pytest.mark.asyncio
async def test_update_assessment_validation_failure(
    handler,
):
    """
    Invalid update should raise ValueError.
    """

    command = UpdateAssessmentCommand(
        assessment_id="",
    )

    with patch(
        "app.application.assessment.handlers.update_assessment_handler.AssessmentValidator.validate_update"
    ) as validator:

        validator.return_value.has_errors.return_value = True

        validator.return_value.error_messages.return_value = (
            "Validation failed."
        )

        with pytest.raises(ValueError):

            await handler.handle(command)


@pytest.mark.asyncio
async def test_update_assessment_not_found(
    handler,
    unit_of_work,
):
    """
    Missing assessment should raise NotFoundException.
    """

    unit_of_work.assessment_repository.get_by_id.return_value = None

    command = UpdateAssessmentCommand(
        assessment_id="00000000-0000-0000-0000-000000000002",
    )

    with patch(
        "app.application.assessment.handlers.update_assessment_handler.AssessmentValidator.validate_update"
    ) as validator:

        validator.return_value.has_errors.return_value = False

        with pytest.raises(NotFoundException):

            await handler.handle(command)