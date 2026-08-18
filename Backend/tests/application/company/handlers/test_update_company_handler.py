"""
Tests for UpdateCompanyHandler.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, Mock

import pytest

from app.application.common.exceptions.not_found_exception import (
    NotFoundException,
)
from app.application.company.company_commands import (
    UpdateCompanyCommand,
)
from app.application.company.handlers.update_company_handler import (
    UpdateCompanyHandler,
)
from app.domain.company.entities.company import (
    Company,
)
from app.domain.company.identifiers.company_id import CompanyId


@pytest.fixture
def validator():
    return Mock()


@pytest.fixture
def mapper():
    mapper = Mock()

    mapper.to_response.return_value = Mock(id="1")
    mapper.to_response.return_value.name = "Updated Company"

    return mapper


@pytest.fixture
def unit_of_work():
    uow = AsyncMock()

    uow.__aenter__.return_value = uow
    uow.__aexit__.return_value = False

    return uow


@pytest.fixture
def handler(
    validator,
    mapper,
    unit_of_work,
):
    return UpdateCompanyHandler(
        unit_of_work=unit_of_work,
        validator=validator,
        mapper=mapper,
    )


@pytest.mark.asyncio
async def test_update_company_success(
    handler,
    validator,
    mapper,
    unit_of_work,
):
    """
    Existing company should be updated.
    """

    company = Mock(spec=Company)
    company.id = CompanyId("00000000-0000-0000-0000-000000000001")

    unit_of_work.company_repository.get_by_id.return_value = company
    unit_of_work.company_repository.find_by_name.return_value = None

    command = UpdateCompanyCommand(
        company_id="00000000-0000-0000-0000-000000000001",
        name="Updated Company",
    )

    result = await handler.handle(command)

    validator.validate_update.assert_called_once_with(command)

    unit_of_work.company_repository.update.assert_awaited_once()

    mapper.to_response.assert_called_once()

    assert result.name == "Updated Company"


@pytest.mark.asyncio
async def test_update_company_not_found(
    handler,
    unit_of_work,
):
    """
    Updating a missing company should raise NotFoundException.
    """

    unit_of_work.company_repository.get_by_id.return_value = None

    command = UpdateCompanyCommand(
        company_id="00000000-0000-0000-0000-000000000999",
        name="Updated",
    )

    with pytest.raises(NotFoundException):
        await handler.handle(command)
