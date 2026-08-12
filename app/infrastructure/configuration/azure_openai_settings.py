"""
Configuration for the Azure OpenAI integration.

Follows the same pydantic-settings pattern as
``app.infrastructure.configuration.database_settings.DatabaseSettings``:
values are read from real process environment variables first, falling
back to a local ``.env`` file if present.

``azure_openai_model`` holds the Azure *deployment* name (the name given
to a deployed model in the Azure OpenAI resource), not a raw model family
name -- Azure OpenAI routes requests by deployment, not by base model.
"""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class AzureOpenAISettings(BaseSettings):
    """Azure OpenAI API configuration."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    azure_openai_api_key: str = ""
    azure_openai_endpoint: str = ""
    azure_openai_api_version: str = "2025-01-01-preview"
    azure_openai_model: str = "gpt-4.1"
