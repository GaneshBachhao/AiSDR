"""
Configuration for the Gemini AI integration.

Follows the same pydantic-settings pattern as
``app.infrastructure.configuration.database_settings.DatabaseSettings``:
values are read from real process environment variables first, falling
back to a local ``.env`` file if present.
"""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class GeminiSettings(BaseSettings):
    """Gemini API configuration."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.5-flash"

    # Optional second key -- GeminiClient fails over to it automatically on a
    # real 429/RESOURCE_EXHAUSTED from the first. Empty (default) = the
    # feature is inert, identical to single-key behavior.
    gemini_api_key_2: str = ""
