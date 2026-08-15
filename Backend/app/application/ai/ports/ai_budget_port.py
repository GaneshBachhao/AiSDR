"""
Application port for pre-flight AI budget enforcement.

Decouples callers (e.g. ``SearchCompaniesHandler``) from the concrete
usage-tracking/persistence mechanism. Implementations live in the
infrastructure layer.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class AIBudgetPort(ABC):
    """Application port for checking a batch of AI calls against budget."""

    @abstractmethod
    async def ensure_batch_fits(
        self,
        provider: str,
        requested_count: int,
    ) -> None:
        """Raise if ``requested_count`` calls against ``provider`` would
        exceed today's remaining budget. No-op if unlimited or unconfigured."""
        raise NotImplementedError
