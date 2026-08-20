"""
In-process requests-per-minute throttle for AI provider calls.

Complements AIBudgetGuard (a daily total, checked once before a batch
starts) with a per-minute sliding window, checked before every individual
outbound call -- the gap AIBudgetGuard doesn't cover: concurrent fan-out
(e.g. SearchCompaniesHandler's bounded research tasks) can fire several
calls within the same second, bursting past a free-tier RPM ceiling even
while comfortably under the daily budget.

Unlike AIBudgetGuard, this class is NOT safe to reconstruct per-request --
its state (recent call timestamps) must persist across requests and across
the concurrent tasks within one request to actually limit anything. Callers
must share one instance (see composition.get_ai_rate_limiter()).
"""

from __future__ import annotations

import asyncio
import time
from collections import defaultdict, deque
from collections.abc import Awaitable, Callable

from app.infrastructure.configuration.ai_rate_limit_settings import AIRateLimitSettings

_WINDOW_SECONDS = 60.0


class AIRateLimiter:
    """Per-provider sliding-window requests-per-minute throttle."""

    def __init__(
        self,
        settings: AIRateLimitSettings | None = None,
        clock: Callable[[], float] = time.monotonic,
        sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
    ) -> None:
        self._settings = settings or AIRateLimitSettings()
        self._clock = clock
        self._sleep = sleep
        self._timestamps: dict[str, deque[float]] = defaultdict(deque)
        self._locks: dict[str, asyncio.Lock] = defaultdict(asyncio.Lock)

    async def acquire(self, provider: str) -> None:
        """Block until another call against ``provider`` is allowed this minute.

        No-op immediately if the provider has no configured limit.
        """

        limit = self._settings.rpm_for(provider)
        if limit is None:
            return

        key = provider.strip().lower()
        lock = self._locks[key]

        while True:
            wait_seconds = 0.0
            async with lock:
                window = self._timestamps[key]
                now = self._clock()
                while window and now - window[0] >= _WINDOW_SECONDS:
                    window.popleft()

                if len(window) < limit:
                    window.append(now)
                    return

                wait_seconds = _WINDOW_SECONDS - (now - window[0])

            # Deliberately sleep outside the lock: several waiters on the
            # same provider can each re-check independently as soon as
            # they wake, instead of serializing one full window-wait at a
            # time when some of them could actually proceed together once
            # the window frees up.
            await self._sleep(max(wait_seconds, 0.0))
