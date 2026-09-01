"""
Configuration for the Tavily integration.

Follows the same pydantic-settings pattern as
``app.infrastructure.configuration.database_settings.DatabaseSettings``:
values are read from real process environment variables first, falling
back to a local ``.env`` file if present.
"""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class TavilySettings(BaseSettings):
    """Tavily API configuration."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    tavily_api_key: str = ""

    # Optional second key -- AgneticTavilyClient fails over to it automatically
    # on a real usage-limit/rate-limit error from the first. Empty (default) =
    # the feature is inert, identical to single-key behavior.
    tavily_api_key_2: str = ""
