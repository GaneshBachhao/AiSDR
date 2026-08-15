"""
Tests for DeleteCompanyHandler.
"""

from __future__ import annotations

from unittest.mock import AsyncMock
from unittest.mock import Mock

import pytest

from app.application.common.exceptions.not_found_exception import (
    NotFoundException,
)
from app.application.company.company_commands import (
    DeleteCompanyCommand,
)
from app.application.company.handlers.delete_company_handler import (
    DeleteCompanyHandler,
)
from app.domain.company.entities.company import (
    Company,
)
from app.domain.company.identifiers.company_id import CompanyId


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
    return DeleteCompanyHandler(
        unit_of_work=unit_of_work,
    )


@pytest.mark.asyncio
async def test_delete_company_success(
    handler,
    unit_of_work,
):
    """
    Existing company should be deleted.
    """

    company = Mock(spec=Company)

    unit_of_work.company_repository.get_by_id.return_value = company

    command = DeleteCompanyCommand(
        company_id="00000000-0000-0000-0000-000000000001",
    )

    await handler.handle(command)

    unit_of_work.company_repository.delete.assert_awaited_once_with(
        CompanyId("00000000-0000-0000-0000-000000000001"),
    )


@pytest.mark.asyncio
async def test_delete_company_not_found(
    handler,
    unit_of_work,
):
    """
    Deleting a missing company should raise NotFoundException.
    """

    unit_of_work.company_repository.get_by_id.return_value = None

    command = DeleteCompanyCommand(
        company_id="00000000-0000-0000-0000-000000000999",
    )

    with pytest.raises(NotFoundException):
        await handler.handle(command)