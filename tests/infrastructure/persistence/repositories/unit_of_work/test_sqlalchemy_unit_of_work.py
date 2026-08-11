"""
Tests for SqlAlchemyUnitOfWork.
"""

from __future__ import annotations

import pytest

from app.domain.company.entities.company import Company
from app.infrastructure.persistence.unit_of_work.sqlalchemy_unit_of_work import (
    SqlAlchemyUnitOfWork,
)


@pytest.mark.asyncio
async def test_commit_persists_company(async_session_factory):
    uow = SqlAlchemyUnitOfWork(async_session_factory)

    async with uow:
        company = Company(name="Commit Test")
        await uow.companies.add(company)

    async with uow:
        loaded = await uow.companies.get_by_id(company.id)

    assert loaded is not None
    assert loaded.name == "Commit Test"


@pytest.mark.asyncio
async def test_repository_is_available(async_session_factory):
    uow = SqlAlchemyUnitOfWork(async_session_factory)

    async with uow:
        assert uow.companies is not None


@pytest.mark.asyncio
async def test_multiple_operations(async_session_factory):
    uow = SqlAlchemyUnitOfWork(async_session_factory)

    async with uow:
        await uow.companies.add(Company(name="Company A"))
        await uow.companies.add(Company(name="Company B"))

    async with uow:
        companies = await uow.companies.list()

    assert len(companies) >= 2


@pytest.mark.asyncio
async def test_update_company(async_session_factory):
    uow = SqlAlchemyUnitOfWork(async_session_factory)

    async with uow:
        company = Company(name="Old")
        await uow.companies.add(company)

    company.rename("New")

    async with uow:
        await uow.companies.update(company)

    async with uow:
        loaded = await uow.companies.get_by_id(company.id)

    assert loaded.name == "New"


@pytest.mark.asyncio
async def test_delete_company(async_session_factory):
    uow = SqlAlchemyUnitOfWork(async_session_factory)

    async with uow:
        company = Company(name="Delete")
        await uow.companies.add(company)

    async with uow:
        loaded = await uow.companies.get_by_id(company.id)
        await uow.companies.delete(loaded)

    async with uow:
        loaded = await uow.companies.get_by_id(company.id)

    assert loaded is None