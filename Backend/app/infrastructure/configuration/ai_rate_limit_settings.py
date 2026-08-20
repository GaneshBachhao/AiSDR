"""
Per-provider AI requests-per-minute limits.

Gemini's default (5) matches the real free-tier RPM ceiling -- distinct
from AIBudgetSettings' *daily* totals, this covers the burst case where
several concurrent AI calls (e.g. SearchCompaniesHandler's bounded
research fan-out) fire within the same minute.
"""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class AIRateLimitSettings(BaseSettings):
    """Reads ``AI_RATE_LIMIT_RPM_<PROVIDER>`` from the environment/.env file.

    A value of ``0`` means "not limited / unlimited" for that provider.
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    ai_rate_limit_rpm_gemini: int = 5
    ai_rate_limit_rpm_openai: int = 0
    ai_rate_limit_rpm_azure_openai: int = 0

    def rpm_for(self, provider: str) -> int | None:
        """Return the configured requests-per-minute limit for ``provider``, or ``None`` if unlimited."""

        field_name = f"ai_rate_limit_rpm_{provider.strip().lower()}"
        value = getattr(self, field_name, 0)
        return value if value > 0 else None
