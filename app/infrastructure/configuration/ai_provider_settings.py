"""
Application-wide default AI provider selection.

Single source of truth for which configured provider
(``app.infrastructure.ai.composition.build_ai_providers``) is used when a
caller does not choose one explicitly. Any module that needs an AI provider
should read this instead of defining its own provider-selection setting.
"""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class AIProviderSettings(BaseSettings):
    """Reads ``AI_PROVIDER`` from the environment/.env file."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    ai_provider: str = "gemini"
