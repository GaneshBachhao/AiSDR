"""
Tests for GetCompanyHandler.
"""

from __future__ import annotations

from unittest.mock import AsyncMock
from unittest.mock import Mock

import pytest

from app.application.common.exceptions.not_found_exception import (
    NotFoundException,
)
from app.application.company.company_queries import (
    GetCompanyQuery,
)
from app.application.company.handlers.get_company_handler import (
    GetCompanyHandler,
)
from app.domain.company.entities.company import (
    Company,
)


@pytest.fixture
def mapper():
    mapper = Mock()

    mapper.to_response.return_value = Mock(id="1")
    mapper.to_response.return_value.name = "OpenAI"

    return mapper


@pytest.fixture
def unit_of_work():

    uow = AsyncMock()

    uow.__aenter__.return_value = uow
    uow.__aexit__.return_value = False

    return uow


@pytest.fixture
def handler(
    mapper,
    unit_of_work,
):

    return GetCompanyHandler(
        unit_of_work=unit_of_work,
        mapper=mapper,
    )


@pytest.mark.asyncio
async def test_get_company_success(
    handler,
    mapper,
    unit_of_work,
):
    """
    Existing company should be returned.
    """

    company = Mock(spec=Company)

    unit_of_work.company_repository.get_by_id.return_value = company

    query = GetCompanyQuery(
        company_id="00000000-0000-0000-0000-000000000001",
    )

    result = await handler.handle(query)

    unit_of_work.company_repository.get_by_id.assert_awaited_once()

    mapper.to_response.assert_called_once_with(company)

    assert result.name == "OpenAI"


@pytest.mark.asyncio
async def test_get_company_not_found(
    handler,
    unit_of_work,
):
    """
    Missing company should raise NotFoundException.
    """

    unit_of_work.company_repository.get_by_id.return_value = None

    query = GetCompanyQuery(
        company_id="00000000-0000-0000-0000-000000000999",
    )

    with pytest.raises(NotFoundException):
        await handler.handle(query)