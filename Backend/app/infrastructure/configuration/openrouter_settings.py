"""
Configuration for the OpenRouter integration.

OpenRouter (https://openrouter.ai) is a unified API gateway in front of many
models, including genuinely free ones -- used here as a Gemini fallback
provider, distinct from the excluded-on-purpose direct OpenAI/Azure OpenAI
providers (see AI_PROVIDER_FALLBACK's comment in .env for why).

Follows the same pydantic-settings pattern as
``app.infrastructure.configuration.database_settings.DatabaseSettings``:
values are read from real process environment variables first, falling
back to a local ``.env`` file if present.
"""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class OpenRouterSettings(BaseSettings):
    """OpenRouter API configuration."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    openrouter_api_key: str = ""
    # A free-tier ("...:free") model id -- OpenRouter's free-model catalog
    # changes over time, so double-check this is still live at
    # https://openrouter.ai/models?max_price=0 before relying on it.
    openrouter_model: str = "meta-llama/llama-3.3-70b-instruct:free"
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
