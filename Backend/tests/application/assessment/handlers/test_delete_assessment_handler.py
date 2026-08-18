"""
Tests for DeleteAssessmentHandler.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, Mock

import pytest

from app.application.assessment.handlers.delete_assessment_handler import (
    DeleteAssessmentHandler,
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

    return DeleteAssessmentHandler(
        unit_of_work=unit_of_work,
    )


@pytest.mark.asyncio
async def test_delete_assessment_success(
    handler,
    unit_of_work,
):
    """
    Assessment should be deleted successfully.
    """

    assessment = Mock()

    unit_of_work.assessment_repository.get_by_id.return_value = assessment

    await handler.handle("00000000-0000-0000-0000-000000000002")

    unit_of_work.assessment_repository.get_by_id.assert_awaited_once()

    unit_of_work.assessment_repository.delete.assert_awaited_once_with(
        assessment,
    )


@pytest.mark.asyncio
async def test_delete_assessment_not_found(
    handler,
    unit_of_work,
):
    """
    Missing assessment should raise NotFoundException.
    """

    unit_of_work.assessment_repository.get_by_id.return_value = None

    with pytest.raises(NotFoundException):
        await handler.handle("00000000-0000-0000-0000-000000000002")
