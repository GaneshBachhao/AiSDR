"""
JWT access-token encode/decode, backed by PyJWT.

No refresh-token flow -- access tokens are the only token this service
issues, per the v1 design decision recorded in the auth implementation
plan (see PARK-F-AUTH). Decode failures (invalid signature, malformed
token, expired token) are raised as jwt.PyJWTError subclasses -- callers
translate those into the application's own UnauthorizedException; this
service stays exception-family-agnostic like every other infrastructure
class in this codebase.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import jwt

from app.infrastructure.configuration.jwt_settings import JWTSettings


class JWTService:
    """Encodes and decodes JWT access tokens."""

    def __init__(self, settings: JWTSettings) -> None:
        self._settings = settings

    def encode(self, subject: str) -> str:
        now = datetime.now(UTC)
        payload = {
            "sub": subject,
            "iat": now,
            "exp": now + timedelta(minutes=self._settings.jwt_access_token_expire_minutes),
        }
        return jwt.encode(
            payload,
            self._settings.jwt_secret_key,
            algorithm=self._settings.jwt_algorithm,
        )

    def decode(self, token: str) -> dict:
        return jwt.decode(
            token,
            self._settings.jwt_secret_key,
            algorithms=[self._settings.jwt_algorithm],
        )

    @property
    def expire_minutes(self) -> int:
        return self._settings.jwt_access_token_expire_minutes
