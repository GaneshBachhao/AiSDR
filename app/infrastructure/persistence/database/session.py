"""
Database session management.

Provides SQLAlchemy engine and session factory
for infrastructure persistence operations.
"""

from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config.settings import settings


class DatabaseSessionFactory:
    """
    Creates database sessions.

    Infrastructure layer abstraction responsible
    for database connection lifecycle.
    """

    def __init__(self) -> None:
        self._engine = create_engine(
            settings.DATABASE_URL,
            pool_pre_ping=True,
            echo=False,
        )

        self._session_factory = sessionmaker(
            bind=self._engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        )

    def create_session(self) -> Session:
        """
        Create a new database session.
        """
        return self._session_factory()


database_session_factory = DatabaseSessionFactory()


def get_db_session() -> Generator[Session, None, None]:
    """
    Database session dependency.

    Ensures session cleanup after usage.
    """

    session = database_session_factory.create_session()

    try:
        yield session
    finally:
        session.close()