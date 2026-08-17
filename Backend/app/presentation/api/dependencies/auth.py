"""
Authentication dependencies.

Provides the current authenticated User to FastAPI presentation layer.
Every failure path here -- missing header, malformed token, expired
token, unknown user, inactive user -- raises the SAME UnauthorizedException
message, mirroring LoginHandler's anti-enumeration stance: a caller
probing a stolen/expired token shouldn't be able to tell "the token was
bad" apart from "that user doesn't exist anymore."
"""

from __future__ import annotations

from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.application.common.exceptions.unauthorized_exception import (
    UnauthorizedException,
)
from app.application.common.interfaces.unit_of_work import UnitOfWork
from app.domain.user.entities.user import User
from app.domain.user.identifiers.user_id import UserId
from app.infrastructure.security.jwt_service import JWTService
from app.presentation.api.dependencies.handlers import get_jwt_service
from app.presentation.api.dependencies.persistence import get_unit_of_work

_INVALID_TOKEN_MESSAGE = "Invalid or expired token."

# auto_error=False so a missing header raises OUR UnauthorizedException
# (which maps to a clean 401 response body) instead of FastAPI's default
# unstructured 403.
_bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),
    uow: UnitOfWork = Depends(get_unit_of_work),
    jwt_service: JWTService = Depends(get_jwt_service),
) -> User:
    if credentials is None:
        raise UnauthorizedException("Authentication required.")

    try:
        payload = jwt_service.decode(credentials.credentials)
    except jwt.PyJWTError:
        raise UnauthorizedException(_INVALID_TOKEN_MESSAGE) from None

    subject = payload.get("sub")
    if not subject:
        raise UnauthorizedException(_INVALID_TOKEN_MESSAGE)

    try:
        user_id = UserId(subject)
    except ValueError:
        raise UnauthorizedException(_INVALID_TOKEN_MESSAGE) from None

    async with uow:
        user = await uow.user_repository.get_by_id(user_id)

    if user is None or not user.is_active:
        raise UnauthorizedException(_INVALID_TOKEN_MESSAGE)

    return user


CurrentUserDependency = Annotated[User, Depends(get_current_user)]
