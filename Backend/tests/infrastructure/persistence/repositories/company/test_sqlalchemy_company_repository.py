"""
Tests for SqlAlchemyCompanyRepository.
"""

from __future__ import annotations

import pytest

from app.domain.company.entities.company import Company
from app.infrastructure.persistence.repositories.company.sqlalchemy_company_repository import (
    SqlAlchemyCompanyRepository,
)


@pytest.mark.asyncio
async def test_add_and_get_company(async_session):
    repository = SqlAlchemyCompanyRepository(async_session)

    company = Company(
        name="Microsoft",
        website="https://microsoft.com",
    )

    await repository.add(company)
    await async_session.commit()

    loaded = await repository.get_by_id(company.id)

    assert loaded is not None
    assert loaded.id == company.id
    assert loaded.name == "Microsoft"


@pytest.mark.asyncio
async def test_find_by_name(async_session):
    repository = SqlAlchemyCompanyRepository(async_session)

    company = Company(name="Google")

    await repository.add(company)
    await async_session.commit()

    loaded = await repository.find_by_name("Google")

    assert loaded is not None
    assert loaded.name == "Google"


@pytest.mark.asyncio
async def test_find_by_website(async_session):
    repository = SqlAlchemyCompanyRepository(async_session)

    company = Company(name="Acme Manufacturing", website="https://acme.example")

    await repository.add(company)
    await async_session.commit()

    loaded = await repository.find_by_website("https://acme.example")

    assert loaded is not None
    assert loaded.name == "Acme Manufacturing"


@pytest.mark.asyncio
async def test_find_by_website_returns_none_when_not_found(async_session):
    repository = SqlAlchemyCompanyRepository(async_session)
    assert await repository.find_by_website("https://nowhere.example") is None


@pytest.mark.asyncio
async def test_list_companies(async_session):
    repository = SqlAlchemyCompanyRepository(async_session)

    await repository.add(Company(name="Apple"))
    await repository.add(Company(name="Amazon"))
    await async_session.commit()

    companies = await repository.list()

    assert len(companies) >= 2


@pytest.mark.asyncio
async def test_search_company(async_session):
    repository = SqlAlchemyCompanyRepository(async_session)

    await repository.add(Company(name="OpenAI"))
    await repository.add(Company(name="Microsoft"))
    await async_session.commit()

    companies = await repository.search("Open")

    assert len(companies) == 1
    assert companies[0].name == "OpenAI"


@pytest.mark.asyncio
async def test_update_company(async_session):
    repository = SqlAlchemyCompanyRepository(async_session)

    company = Company(name="Old")

    await repository.add(company)
    await async_session.commit()

    company.rename("New")

    await repository.update(company)
    await async_session.commit()

    loaded = await repository.get_by_id(company.id)

    assert loaded.name == "New"


@pytest.mark.asyncio
async def test_delete_company(async_session):
    repository = SqlAlchemyCompanyRepository(async_session)

    company = Company(name="Delete Me")

    await repository.add(company)
    await async_session.commit()

    await repository.delete(company)
    await async_session.commit()

    loaded = await repository.get_by_id(company.id)

    assert loaded is None