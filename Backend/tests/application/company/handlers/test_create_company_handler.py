"""
Tests for CreateCompanyHandler.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, Mock

import pytest

from app.application.common.exceptions.conflict_exception import (
    ConflictException,
)
from app.application.company.company_commands import (
    CreateCompanyCommand,
)
from app.application.company.handlers.create_company_handler import (
    CreateCompanyHandler,
)
from app.domain.company.entities.company import (
    Company,
)


@pytest.fixture
def validator():
    return Mock()


@pytest.fixture
def mapper():
    mapper = Mock()

    company = Mock(spec=Company)

    mapper.to_domain.return_value = company

    mapper.to_response.return_value = Mock(id="1")
    mapper.to_response.return_value.name = "OpenAI"

    return mapper


@pytest.fixture
def unit_of_work():

    uow = AsyncMock()

    uow.__aenter__.return_value = uow
    uow.__aexit__.return_value = False

    uow.company_repository.find_by_name.return_value = None

    return uow


@pytest.fixture
def handler(
    validator,
    mapper,
    unit_of_work,
):

    return CreateCompanyHandler(
        unit_of_work=unit_of_work,
        validator=validator,
        mapper=mapper,
    )


@pytest.mark.asyncio
async def test_create_company_success(
    handler,
    validator,
    mapper,
    unit_of_work,
):
    """
    Company should be created successfully.
    """

    command = CreateCompanyCommand(
        name="OpenAI",
    )

    result = await handler.handle(command)

    validator.validate_create.assert_called_once_with(command)

    mapper.to_domain.assert_called_once_with(command)

    unit_of_work.company_repository.add.assert_awaited_once()

    mapper.to_response.assert_called_once()

    assert result.name == "OpenAI"


@pytest.mark.asyncio
async def test_duplicate_company_raises_conflict(
    handler,
    unit_of_work,
):
    """
    Duplicate company should raise ConflictException.
    """

    command = CreateCompanyCommand(
        name="OpenAI",
    )

    unit_of_work.company_repository.find_by_name.return_value = Mock()

    with pytest.raises(ConflictException):
        await handler.handle(command)
