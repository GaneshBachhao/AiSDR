"""
Search provider selection (single switch, used app-wide): tavily | ddgs.
"""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class SearchProviderSettings(BaseSettings):
    """Reads ``SEARCH_PROVIDER`` from the environment/.env file."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    search_provider: str = "tavily"
