"""
Application startup and shutdown lifecycle.
"""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.infrastructure.configuration.database_settings import (
    DatabaseSettings,
)

from app.infrastructure.persistence.database.base import (
    Base,
)

from app.infrastructure.persistence.database.engine import (
    get_async_engine,
)

# IMPORTANT:
# Import all SQLAlchemy models so metadata is populated.
from app.infrastructure.persistence import models  # noqa: F401


async def initialize_database() -> None:
    """
    Create database tables if they do not exist.
    """

    settings = DatabaseSettings()

    engine = get_async_engine(
        settings,
    )

    async with engine.begin() as connection:

        await connection.run_sync(
            Base.metadata.create_all,
        )

        # -------------------------------
        # TEMPORARY DEBUG
        # -------------------------------
        from sqlalchemy import text

        result = await connection.execute(
            text("PRAGMA database_list")
        )

        print("\nDATABASE:")
        print(result.fetchall())

        result = await connection.execute(
            text("PRAGMA table_info(assessments)")
        )

        print("\nASSESSMENTS TABLE:")
        for row in result.fetchall():
            print(row)

        print("-" * 80)

async def shutdown_database() -> None:
    """
    Dispose database resources.
    """

    settings = DatabaseSettings()

    engine = get_async_engine(
        settings,
    )

    await engine.dispose()


@asynccontextmanager
async def lifespan(
    app: FastAPI,
):
    """
    Application startup and shutdown lifecycle.
    """

    # ----------------------------
    # Startup
    # ----------------------------

    await initialize_database()


    yield


    # ----------------------------
    # Shutdown
    # ----------------------------

    await shutdown_database()