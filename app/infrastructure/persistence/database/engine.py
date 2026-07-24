"""
SQLAlchemy engine factory.

Creates and manages the application's async database engine.
"""

from __future__ import annotations

from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)

from app.infrastructure.configuration.database_settings import DatabaseSettings


class DatabaseEngine:
    """
    Creates and owns the SQLAlchemy async engine.
    """

    def __init__(self, settings: DatabaseSettings) -> None:
        self._settings = settings
        self._engine: AsyncEngine | None = None
        self._session_factory: async_sessionmaker | None = None

    @property
    def engine(self) -> AsyncEngine:
        """
        Returns the singleton async engine.
        """
        if self._engine is None:
            self._engine = self._create_engine()

        return self._engine

    @property
    def session_factory(self) -> async_sessionmaker:
        """
        Returns the singleton async session factory.
        """
        if self._session_factory is None:
            self._session_factory = async_sessionmaker(
                bind=self.engine,
                autoflush=False,
                expire_on_commit=False,
            )

        return self._session_factory

    async def dispose(self) -> None:
        """
        Dispose the current engine.
        """
        if self._engine is not None:
            await self._engine.dispose()


    

    def _create_engine(self) -> AsyncEngine:
        """
        Build the SQLAlchemy async engine.
        """

        if self._settings.database_url:
            database_url = self._settings.database_url

        else:
            database_url = URL.create(
                drivername=self._settings.driver,
                username=self._settings.username,
                password=self._settings.password,
                host=self._settings.host,
                port=self._settings.port,
                database=self._settings.database,
            )

        return create_async_engine(
            database_url,
            echo=self._settings.echo,
            future=True,
            pool_pre_ping=True,
            pool_size=self._settings.pool_size,
            max_overflow=self._settings.max_overflow,
            pool_recycle=self._settings.pool_recycle,
        )


_database_engine: DatabaseEngine | None = None


def get_database_engine(
    settings: DatabaseSettings,
) -> DatabaseEngine:
    """
    Returns the singleton DatabaseEngine.
    """

    global _database_engine

    if _database_engine is None:
        _database_engine = DatabaseEngine(settings)

    return _database_engine


def get_async_engine(
    settings: DatabaseSettings,
) -> AsyncEngine:
    """
    Dependency helper.
    """

    return get_database_engine(settings).engine


def get_session_factory(
    settings: DatabaseSettings,
) -> async_sessionmaker:
    """
    Dependency helper.
    """

    return get_database_engine(settings).session_factory