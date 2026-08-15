"""
Persistence dependencies.

Provides database session and Unit Of Work
for FastAPI presentation layer.
"""

from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import Annotated
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.configuration.database_settings import (
    DatabaseSettings,
)

from app.infrastructure.persistence.database.session import (
    get_session_manager,
)

from app.infrastructure.persistence.unit_of_work.sqlalchemy_unit_of_work import (
    SqlAlchemyUnitOfWork,
)

from app.application.common.interfaces.unit_of_work import (
    UnitOfWork,
)



def get_database_settings() -> DatabaseSettings:
    """
    Provides database configuration.
    """

    return DatabaseSettings()



async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Provides AsyncSession lifecycle.
    """

    manager = get_session_manager(
        get_database_settings(),
    )

    session = manager.create_session()

    try:
        yield session

    finally:
        await session.close()



async def get_unit_of_work(
    session: AsyncSession = Depends(get_db_session),
) -> UnitOfWork:
    """
    Provides Unit Of Work.
    """

    return SqlAlchemyUnitOfWork(
        session=session,
    )

