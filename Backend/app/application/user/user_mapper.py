"""
User application mapper.

Maps request DTOs -> commands and domain entities -> response DTOs.
"""

from __future__ import annotations

from app.application.user.dto.current_user_response import CurrentUserResponseDTO
from app.application.user.dto.login_request import LoginRequestDTO
from app.application.user.dto.login_response import LoginResponseDTO
from app.application.user.user_commands import LoginCommand
from app.domain.user.entities.user import User


class UserMapper:
    """Maps User application/domain objects."""

    @staticmethod
    def to_login_command(dto: LoginRequestDTO) -> LoginCommand:
        return LoginCommand(email=dto.email, password=dto.password)

    @staticmethod
    def to_current_user_response(user: User) -> CurrentUserResponseDTO:
        return CurrentUserResponseDTO(
            id=str(user.id.value),
            email=user.email.value,
            is_active=user.is_active,
        )

    @staticmethod
    def to_login_response(
        user: User,
        access_token: str,
        expires_in: int,
    ) -> LoginResponseDTO:
        return LoginResponseDTO(
            access_token=access_token,
            expires_in=expires_in,
            user=UserMapper.to_current_user_response(user),
        )
