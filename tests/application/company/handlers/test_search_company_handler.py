"""
Tests for SearchCompanyHandler.
"""

from __future__ import annotations

from unittest.mock import AsyncMock
from unittest.mock import Mock

import pytest

from app.application.company.company_queries import (
    SearchCompaniesQuery,
)
from app.application.company.handlers.search_company_handler import (
    SearchCompanyHandler,
)
from app.domain.company.entities.company import (
    Company,
)


@pytest.fixture
def mapper():
    mapper = Mock()

    openai = Mock(id="1")
    openai.name = "OpenAI"
    mapper.to_response_list.return_value = [openai]

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
    return SearchCompanyHandler(
        unit_of_work=unit_of_work,
        mapper=mapper,
    )


@pytest.mark.asyncio
async def test_search_company_success(
    handler,
    mapper,
    unit_of_work,
):
    """
    Should return matching companies.
    """

    companies = [
        Mock(spec=Company),
    ]

    unit_of_work.company_repository.search.return_value = companies

    query = SearchCompaniesQuery(
        search_text="Open",
        skip=0,
        limit=100,
    )

    result = await handler.handle(query)

    unit_of_work.company_repository.search.assert_awaited_once_with(
        search_text="Open",
        skip=0,
        limit=100,
    )

    mapper.to_response_list.assert_called_once_with(
        companies,
    )

    assert len(result) == 1

    assert result[0].name == "OpenAI"