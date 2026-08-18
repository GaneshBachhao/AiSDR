"""
Tests for ListCompanyHandler.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, Mock

import pytest

from app.application.company.company_queries import (
    ListCompaniesQuery,
)
from app.application.company.handlers.list_company_handler import (
    ListCompanyHandler,
)
from app.domain.company.entities.company import (
    Company,
)


@pytest.fixture
def mapper():
    mapper = Mock()

    openai = Mock(id="1")
    openai.name = "OpenAI"
    microsoft = Mock(id="2")
    microsoft.name = "Microsoft"
    mapper.to_response_list.return_value = [openai, microsoft]

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
    return ListCompanyHandler(
        unit_of_work=unit_of_work,
        mapper=mapper,
    )


@pytest.mark.asyncio
async def test_list_companies(
    handler,
    mapper,
    unit_of_work,
):
    """
    Should return all companies.
    """

    companies = [
        Mock(spec=Company),
        Mock(spec=Company),
    ]

    unit_of_work.company_repository.list.return_value = companies

    query = ListCompaniesQuery(
        skip=0,
        limit=100,
    )

    result = await handler.handle(query)

    unit_of_work.company_repository.list.assert_awaited_once_with(
        skip=0,
        limit=100,
    )

    mapper.to_response_list.assert_called_once_with(
        companies,
    )

    assert len(result) == 2

    assert result[0].name == "OpenAI"

    assert result[1].name == "Microsoft"
