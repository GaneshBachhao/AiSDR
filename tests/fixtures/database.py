"""
Database fixtures.
"""

from __future__ import annotations

import pytest_asyncio

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
)

from app.infrastructure.persistence.database.base import Base


TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture
async def engine() -> AsyncEngine:
    engine = create_async_engine(
        TEST_DATABASE_URL,
        future=True,
    )

    async with engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.create_all,
        )

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()