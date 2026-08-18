"""
Unit of Work fixtures.
"""

from __future__ import annotations

import pytest_asyncio

from app.infrastructure.persistence.unit_of_work.sqlalchemy_unit_of_work import (
    SqlAlchemyUnitOfWork,
)


@pytest_asyncio.fixture
async def unit_of_work(
    async_session_factory,
):
    yield SqlAlchemyUnitOfWork(
        async_session_factory,
    )
