"""
Login handler.
"""

from __future__ import annotations

from app.application.common.exceptions.unauthorized_exception import (
    UnauthorizedException,
)
from app.application.common.interfaces.unit_of_work import (
    UnitOfWork,
)
from app.application.user.dto.login_response import LoginResponseDTO
from app.application.user.user_commands import LoginCommand
from app.application.user.user_mapper import UserMapper
from app.domain.user.value_objects.email import Email
from app.infrastructure.security.jwt_service import JWTService
from app.infrastructure.security.password_hasher import PasswordHasher

_INVALID_CREDENTIALS_MESSAGE = "Invalid email or password."


class LoginHandler:
    """
    Handle Login use case.

    Every failure path -- unknown email, malformed email, wrong password,
    an inactive account -- raises the SAME UnauthorizedException message.
    This is deliberate: distinguishing "no such user" from "wrong
    password" in the response would let an attacker enumerate real
    accounts one guess at a time.
    """

    def __init__(
        self,
        unit_of_work: UnitOfWork,
        password_hasher: PasswordHasher,
        jwt_service: JWTService,
    ) -> None:
        self._unit_of_work = unit_of_work
        self._password_hasher = password_hasher
        self._jwt_service = jwt_service

    async def handle(
        self,
        command: LoginCommand,
    ) -> LoginResponseDTO:
        try:
            email = Email(command.email)
        except ValueError:
            raise UnauthorizedException(_INVALID_CREDENTIALS_MESSAGE) from None

        async with self._unit_of_work:
            user = await self._unit_of_work.user_repository.find_by_email(
                email.value,
            )

            if user is None or not user.is_active:
                raise UnauthorizedException(_INVALID_CREDENTIALS_MESSAGE)

            if not self._password_hasher.verify(
                command.password,
                user.password_hash.value,
            ):
                raise UnauthorizedException(_INVALID_CREDENTIALS_MESSAGE)

        token = self._jwt_service.encode(subject=str(user.id.value))

        return UserMapper.to_login_response(
            user,
            access_token=token,
            expires_in=self._jwt_service.expire_minutes * 60,
        )
