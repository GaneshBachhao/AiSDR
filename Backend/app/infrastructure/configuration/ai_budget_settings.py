"""
Per-provider daily AI request budgets.

Gemini's default (20) matches the real free-tier daily limit that caused a
live batch failure earlier in this project -- tracking it is what turns
that into a clear pre-flight message instead of N failed identity
verifications discovered one at a time.
"""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class AIBudgetSettings(BaseSettings):
    """Reads ``AI_DAILY_REQUEST_BUDGET_<PROVIDER>`` from the environment/.env file.

    A value of ``0`` means "not tracked / unlimited" for that provider.
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    ai_daily_request_budget_gemini: int = 20
    ai_daily_request_budget_openai: int = 0
    ai_daily_request_budget_azure_openai: int = 0

    def daily_budget_for(self, provider: str) -> int | None:
        """Return the configured daily budget for ``provider``, or ``None`` if unlimited."""

        field_name = f"ai_daily_request_budget_{provider.strip().lower()}"
        value = getattr(self, field_name, 0)
        return value if value > 0 else None
