"""
Database session factory.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)


def create_session_factory(
    engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    """
    Create SQLAlchemy async session factory.
    """

    return async_sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
    )