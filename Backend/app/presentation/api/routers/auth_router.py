"""
Auth API router.

There is no self-service registration endpoint -- accounts are created
by a human operator (see Backend/scripts/create_user.py).
"""

from __future__ import annotations

from fastapi import APIRouter

from app.application.user.dto.current_user_response import CurrentUserResponseDTO
from app.application.user.dto.login_request import LoginRequestDTO
from app.application.user.dto.login_response import LoginResponseDTO
from app.application.user.user_mapper import UserMapper
from app.presentation.api.dependencies.auth import CurrentUserDependency
from app.presentation.api.dependencies.handlers import LoginHandlerDependency

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/login",
    response_model=LoginResponseDTO,
)
async def login(
    request: LoginRequestDTO,
    handler: LoginHandlerDependency,
) -> LoginResponseDTO:
    command = UserMapper.to_login_command(request)
    return await handler.handle(command)


@router.get(
    "/me",
    response_model=CurrentUserResponseDTO,
)
async def get_me(
    current_user: CurrentUserDependency,
) -> CurrentUserResponseDTO:
    return UserMapper.to_current_user_response(current_user)
