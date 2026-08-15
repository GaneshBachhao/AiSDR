"""
Pre-flight AI budget enforcement.

Checks a projected batch of AI calls against the configured daily budget
*before* any call is made, so a batch that would exceed quota fails once,
clearly, instead of partway through as N near-identical per-call failures.
"""

from __future__ import annotations

from app.application.ai.ports.ai_budget_port import AIBudgetPort
from app.infrastructure.ai.exceptions.ai_budget_exceeded_exception import (
    AIBudgetExceededException,
)
from app.infrastructure.ai.usage.ai_usage_tracker import AIUsageTracker
from app.infrastructure.configuration.ai_budget_settings import AIBudgetSettings


class AIBudgetGuard(AIBudgetPort):
    """Combines usage tracking with configured budgets to gate AI batches."""

    def __init__(
        self,
        tracker: AIUsageTracker,
        settings: AIBudgetSettings | None = None,
    ) -> None:
        self._tracker = tracker
        self._settings = settings or AIBudgetSettings()

    async def remaining_budget(self, provider: str) -> int | None:
        """Return remaining calls today for ``provider``, or ``None`` if unlimited."""

        budget = self._settings.daily_budget_for(provider)

        if budget is None:
            return None

        used = await self._tracker.count_requests_today(provider)
        return max(budget - used, 0)

    async def ensure_batch_fits(self, provider: str, requested_count: int) -> None:
        """Raise ``AIBudgetExceededException`` if ``requested_count`` calls
        against ``provider`` would exceed today's remaining budget."""

        if requested_count <= 0:
            return

        remaining = await self.remaining_budget(provider)

        if remaining is None or requested_count <= remaining:
            return

        budget = self._settings.daily_budget_for(provider)
        raise AIBudgetExceededException(
            f"Requested {requested_count} AI calls against '{provider}' but "
            f"only {remaining} remain in today's budget ({budget}/day). "
            "Reduce number_of_companies, wait for the daily reset, or "
            "configure AI_PROVIDER_FALLBACK with a provider that has budget."
        )
