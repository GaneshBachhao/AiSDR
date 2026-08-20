"""
Configuration for webhook shared-secret verification.

Follows the same pydantic-settings pattern as
``app.infrastructure.configuration.jwt_settings.JWTSettings``: values are
read from real process environment variables first, falling back to a
local ``.env`` file if present.
"""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class WebhookSettings(BaseSettings):
    """Shared-secret configuration for third-party webhook endpoints."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    email_webhook_secret: str = ""
