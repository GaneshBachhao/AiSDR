"""
Shared pytest fixtures.

Provides an isolated in-memory SQLite database
for repository and service tests.
"""

import pytest
import app.models

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.database import Base


# ==========================================================
# Test Engine
# ==========================================================

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# ==========================================================
# Database Fixture
# ==========================================================

@pytest.fixture
def db_session():
    """
    Creates a fresh database for every test.
    """

    Base.metadata.create_all(
        bind=engine,
    )

    db = TestingSessionLocal()

    try:

        yield db

    finally:

        db.close()

        Base.metadata.drop_all(
            bind=engine,
        )