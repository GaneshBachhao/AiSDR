"""
Session fixtures.
"""

from __future__ import annotations

import pytest_asyncio
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
)


@pytest_asyncio.fixture
async def async_session_factory(engine):
    return async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )


@pytest_asyncio.fixture
async def async_session(async_session_factory):
    async with async_session_factory() as session:
        yield session
