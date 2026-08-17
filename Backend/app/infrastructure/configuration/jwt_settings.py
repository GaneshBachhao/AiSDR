"""
Configuration for JWT session tokens.

Follows the same pydantic-settings pattern as
``app.infrastructure.configuration.gemini_settings.GeminiSettings``:
values are read from real process environment variables first, falling
back to a local ``.env`` file if present.
"""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class JWTSettings(BaseSettings):
    """JWT access token configuration."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    jwt_secret_key: str = ""
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 480
