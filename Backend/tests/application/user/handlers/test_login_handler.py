"""
Tests for LoginHandler.
"""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from app.application.common.exceptions.unauthorized_exception import (
    UnauthorizedException,
)
from app.application.user.handlers.login_handler import LoginHandler
from app.application.user.user_commands import LoginCommand
from app.domain.user.entities.user import User
from app.domain.user.value_objects.email import Email
from app.domain.user.value_objects.password_hash import PasswordHash
from app.infrastructure.configuration.jwt_settings import JWTSettings
from app.infrastructure.security.jwt_service import JWTService
from app.infrastructure.security.password_hasher import PasswordHasher


@pytest.fixture
def unit_of_work():
    uow = AsyncMock()
    uow.__aenter__.return_value = uow
    uow.__aexit__.return_value = False
    return uow


@pytest.fixture
def password_hasher():
    return PasswordHasher()


@pytest.fixture
def jwt_service():
    return JWTService(JWTSettings(jwt_secret_key="test-secret"))


@pytest.fixture
def handler(unit_of_work, password_hasher, jwt_service):
    return LoginHandler(
        unit_of_work=unit_of_work,
        password_hasher=password_hasher,
        jwt_service=jwt_service,
    )


def _real_user(password_hasher: PasswordHasher, *, active: bool = True) -> User:
    return User(
        email=Email("jane@example.com"),
        password_hash=PasswordHash(password_hasher.hash("correct-password")),
        is_active=active,
    )


@pytest.mark.asyncio
async def test_login_success_returns_a_token(handler, unit_of_work, password_hasher):
    user = _real_user(password_hasher)
    unit_of_work.user_repository.find_by_email.return_value = user

    command = LoginCommand(email="jane@example.com", password="correct-password")
    result = await handler.handle(command)

    assert result.access_token
    assert result.token_type == "bearer"
    assert result.user.email == "jane@example.com"


@pytest.mark.asyncio
async def test_login_unknown_email_raises_unauthorized(handler, unit_of_work):
    unit_of_work.user_repository.find_by_email.return_value = None

    command = LoginCommand(email="nobody@example.com", password="anything")

    with pytest.raises(UnauthorizedException) as exc_info_unknown:
        await handler.handle(command)

    unknown_message = str(exc_info_unknown.value)

    unit_of_work.user_repository.find_by_email.return_value = None
    with pytest.raises(UnauthorizedException) as exc_info_missing:
        await handler.handle(
            LoginCommand(email="also-nobody@example.com", password="anything")
        )

    assert unknown_message == str(exc_info_missing.value)


@pytest.mark.asyncio
async def test_login_wrong_password_raises_unauthorized_with_the_same_message_as_unknown_email(
    handler,
    unit_of_work,
    password_hasher,
):
    user = _real_user(password_hasher)
    unit_of_work.user_repository.find_by_email.return_value = user

    with pytest.raises(UnauthorizedException) as wrong_password_exc:
        await handler.handle(
            LoginCommand(email="jane@example.com", password="totally-wrong")
        )

    unit_of_work.user_repository.find_by_email.return_value = None
    with pytest.raises(UnauthorizedException) as unknown_email_exc:
        await handler.handle(
            LoginCommand(email="nobody@example.com", password="anything")
        )

    assert str(wrong_password_exc.value) == str(unknown_email_exc.value)


@pytest.mark.asyncio
async def test_login_inactive_user_raises_unauthorized(handler, unit_of_work, password_hasher):
    user = _real_user(password_hasher, active=False)
    unit_of_work.user_repository.find_by_email.return_value = user

    with pytest.raises(UnauthorizedException):
        await handler.handle(
            LoginCommand(email="jane@example.com", password="correct-password")
        )


@pytest.mark.asyncio
async def test_login_malformed_email_raises_unauthorized_not_a_raw_value_error(
    handler,
    unit_of_work,
):
    command = LoginCommand(email="not-an-email", password="anything")

    with pytest.raises(UnauthorizedException):
        await handler.handle(command)

    unit_of_work.user_repository.find_by_email.assert_not_awaited()
