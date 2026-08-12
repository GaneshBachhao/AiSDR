"""
AI provider usage tracking.

Records one row per AI call (success or failure) so downstream code can
answer "how many calls has provider X made today" -- the basis for the
pre-flight budget check in ``AIBudgetGuard``. Deliberately independent of
any FastAPI-injected, request-scoped session: ``AIExecutionService`` may be
invoked many times concurrently within a single request (bounded-concurrency
fan-out in ``SearchCompaniesHandler``), and a single ``AsyncSession`` is not
safe to use from multiple coroutines at once. Each write/read here opens and
closes its own short-lived session instead.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime

from sqlalchemy import func, select

from app.application.ai.ports.ai_usage_recorder import AIUsageRecorder
from app.domain.ai.aggregates.ai_request import AIRequest
from app.infrastructure.configuration.database_settings import DatabaseSettings
from app.infrastructure.persistence.database.session import (
    DatabaseSessionManager,
    get_session_manager,
)
from app.infrastructure.persistence.models.ai_usage_log_model import (
    AIUsageLogModel,
)

logger = logging.getLogger(__name__)


class AIUsageTracker(AIUsageRecorder):
    """Logs AI calls and answers usage queries against ``ai_usage_log``."""

    def __init__(
        self,
        session_manager: DatabaseSessionManager | None = None,
    ) -> None:
        self._session_manager = session_manager or get_session_manager(
            DatabaseSettings()
        )

    async def log(self, request: AIRequest) -> None:
        """Persist one usage row for a completed or failed request.

        Never raises -- a logging failure must not break the underlying AI
        call it's observing.
        """

        usage = request.response.token_usage if request.response else None

        model = AIUsageLogModel(
            provider=request.provider.value.lower(),
            model=str(request.model),
            status=request.status.value,
            prompt_tokens=usage.prompt_tokens if usage else 0,
            completion_tokens=usage.completion_tokens if usage else 0,
            total_tokens=usage.total_tokens if usage else 0,
            created_at=datetime.now(UTC),
        )

        session = None
        try:
            session = self._session_manager.create_session()
            session.add(model)
            await session.commit()
        except Exception:
            logger.warning(
                "Failed to persist AI usage log for provider %r",
                request.provider.value,
                exc_info=True,
            )
        finally:
            if session is not None:
                await session.close()

    async def count_requests_today(self, provider: str) -> int:
        """Count usage rows for ``provider`` since midnight UTC."""

        start_of_day = datetime.now(UTC).replace(
            hour=0, minute=0, second=0, microsecond=0
        )

        session = self._session_manager.create_session()
        try:
            result = await session.execute(
                select(func.count())
                .select_from(AIUsageLogModel)
                .where(
                    AIUsageLogModel.provider == provider.strip().lower(),
                    AIUsageLogModel.created_at >= start_of_day,
                )
            )
            return result.scalar_one()
        finally:
            await session.close()
