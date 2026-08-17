"""
Tests for SqlAlchemyUserRepository.
"""

from __future__ import annotations

import pytest
from sqlalchemy.exc import IntegrityError

from app.domain.user.entities.user import User
from app.domain.user.value_objects.email import Email
from app.domain.user.value_objects.password_hash import PasswordHash
from app.infrastructure.persistence.repositories.user.sqlalchemy_user_repository import (
    SqlAlchemyUserRepository,
)

_VALID_HASH = "$2b$12$" + ("N" * 53)


def _make_user(email: str = "jane@example.com") -> User:
    return User(
        email=Email(email),
        password_hash=PasswordHash(_VALID_HASH),
    )


@pytest.mark.asyncio
async def test_add_and_get_by_id(async_session):
    repository = SqlAlchemyUserRepository(async_session)

    user = _make_user()

    await repository.add(user)
    await async_session.commit()

    loaded = await repository.get_by_id(user.id)

    assert loaded is not None
    assert loaded.id == user.id
    assert loaded.email == user.email


@pytest.mark.asyncio
async def test_find_by_email_hit(async_session):
    repository = SqlAlchemyUserRepository(async_session)

    user = _make_user("jane@example.com")

    await repository.add(user)
    await async_session.commit()

    loaded = await repository.find_by_email("Jane@Example.com")

    assert loaded is not None
    assert loaded.id == user.id


@pytest.mark.asyncio
async def test_find_by_email_miss(async_session):
    repository = SqlAlchemyUserRepository(async_session)

    assert await repository.find_by_email("nobody@example.com") is None


@pytest.mark.asyncio
async def test_duplicate_email_raises_integrity_error(async_session):
    repository = SqlAlchemyUserRepository(async_session)

    await repository.add(_make_user("dupe@example.com"))
    await async_session.commit()

    await repository.add(_make_user("dupe@example.com"))
    with pytest.raises(IntegrityError):
        await async_session.commit()


@pytest.mark.asyncio
async def test_update_user(async_session):
    repository = SqlAlchemyUserRepository(async_session)

    user = _make_user()
    await repository.add(user)
    await async_session.commit()

    user.deactivate()
    await repository.update(user)
    await async_session.commit()

    loaded = await repository.get_by_id(user.id)

    assert loaded.is_active is False
