"""
Tests for GetAssessmentHandler.
"""

from __future__ import annotations

from unittest.mock import AsyncMock
from unittest.mock import Mock
from unittest.mock import patch

import pytest

from app.application.assessment.assessment_queries import (
    GetAssessmentQuery,
)
from app.application.assessment.handlers.get_assessment_handler import (
    GetAssessmentHandler,
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

    return GetAssessmentHandler(
        unit_of_work=unit_of_work,
    )


@pytest.mark.asyncio
async def test_get_assessment_success(
    handler,
    unit_of_work,
):
    """
    Assessment should be returned successfully.
    """

    assessment = Mock()

    unit_of_work.assessment_repository.get_by_id.return_value = (
        assessment
    )

    query = GetAssessmentQuery(
        assessment_id="00000000-0000-0000-0000-000000000002",
    )

    with patch(
        "app.application.assessment.handlers.get_assessment_handler.AssessmentMapper.to_get_response"
    ) as mapper:

        mapper.return_value = "response"

        result = await handler.handle(query)

    unit_of_work.assessment_repository.get_by_id.assert_awaited_once()

    mapper.assert_called_once_with(
        assessment,
    )

    assert result == "response"


@pytest.mark.asyncio
async def test_get_assessment_not_found(
    handler,
    unit_of_work,
):
    """
    Missing assessment should raise NotFoundException.
    """

    unit_of_work.assessment_repository.get_by_id.return_value = None

    query = GetAssessmentQuery(
        assessment_id="00000000-0000-0000-0000-000000000002",
    )

    with pytest.raises(NotFoundException):

        await handler.handle(query)