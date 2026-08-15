from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from app.infrastructure.ai.exceptions.ai_budget_exceeded_exception import (
    AIBudgetExceededException,
)
from app.infrastructure.ai.usage.ai_budget_guard import AIBudgetGuard
from app.infrastructure.configuration.ai_budget_settings import AIBudgetSettings


def _settings(**overrides) -> AIBudgetSettings:
    defaults = dict(
        ai_daily_request_budget_gemini=20,
        ai_daily_request_budget_openai=0,
        ai_daily_request_budget_azure_openai=0,
    )
    defaults.update(overrides)
    return AIBudgetSettings(**defaults)


@pytest.mark.asyncio
async def test_remaining_budget_subtracts_usage_so_far():
    tracker = AsyncMock()
    tracker.count_requests_today.return_value = 12
    guard = AIBudgetGuard(tracker=tracker, settings=_settings())

    assert await guard.remaining_budget("gemini") == 8


@pytest.mark.asyncio
async def test_remaining_budget_never_negative():
    tracker = AsyncMock()
    tracker.count_requests_today.return_value = 25
    guard = AIBudgetGuard(tracker=tracker, settings=_settings())

    assert await guard.remaining_budget("gemini") == 0


@pytest.mark.asyncio
async def test_remaining_budget_none_when_unlimited():
    tracker = AsyncMock()
    guard = AIBudgetGuard(tracker=tracker, settings=_settings())

    assert await guard.remaining_budget("openai") is None
    tracker.count_requests_today.assert_not_awaited()


@pytest.mark.asyncio
async def test_ensure_batch_fits_passes_when_under_budget():
    tracker = AsyncMock()
    tracker.count_requests_today.return_value = 5
    guard = AIBudgetGuard(tracker=tracker, settings=_settings())

    await guard.ensure_batch_fits("gemini", 10)  # 20 - 5 = 15 remaining, fits


@pytest.mark.asyncio
async def test_ensure_batch_fits_raises_when_over_budget():
    tracker = AsyncMock()
    tracker.count_requests_today.return_value = 18
    guard = AIBudgetGuard(tracker=tracker, settings=_settings())

    with pytest.raises(AIBudgetExceededException, match="only 2 remain"):
        await guard.ensure_batch_fits("gemini", 5)


@pytest.mark.asyncio
async def test_ensure_batch_fits_noop_for_unlimited_provider():
    tracker = AsyncMock()
    guard = AIBudgetGuard(tracker=tracker, settings=_settings())

    await guard.ensure_batch_fits("openai", 1000)  # unlimited, must not raise


@pytest.mark.asyncio
async def test_ensure_batch_fits_noop_for_zero_or_negative_request_count():
    tracker = AsyncMock()
    tracker.count_requests_today.return_value = 20
    guard = AIBudgetGuard(tracker=tracker, settings=_settings())

    await guard.ensure_batch_fits("gemini", 0)
    tracker.count_requests_today.assert_not_awaited()
