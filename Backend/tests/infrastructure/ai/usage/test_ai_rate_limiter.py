from __future__ import annotations

import pytest

from app.infrastructure.ai.usage.ai_rate_limiter import AIRateLimiter
from app.infrastructure.configuration.ai_rate_limit_settings import AIRateLimitSettings


class _FakeClock:
    """Injectable clock/sleep pair -- sleeping advances the fake clock
    instead of waiting on the real wall clock, so these tests run instantly
    regardless of the configured window (60s)."""

    def __init__(self, start: float = 0.0) -> None:
        self.now = start
        self.sleep_calls: list[float] = []

    def __call__(self) -> float:
        return self.now

    async def sleep(self, seconds: float) -> None:
        self.sleep_calls.append(seconds)
        self.now += seconds


def _settings(**overrides) -> AIRateLimitSettings:
    defaults = dict(
        ai_rate_limit_rpm_gemini=3,
        ai_rate_limit_rpm_openai=0,
        ai_rate_limit_rpm_azure_openai=0,
    )
    defaults.update(overrides)
    return AIRateLimitSettings(**defaults)


@pytest.mark.asyncio
async def test_calls_within_the_limit_never_wait():
    clock = _FakeClock()
    limiter = AIRateLimiter(settings=_settings(), clock=clock, sleep=clock.sleep)

    await limiter.acquire("gemini")
    await limiter.acquire("gemini")
    await limiter.acquire("gemini")

    assert clock.sleep_calls == []


@pytest.mark.asyncio
async def test_the_call_over_the_limit_waits_for_the_window_to_free_up():
    clock = _FakeClock()
    limiter = AIRateLimiter(settings=_settings(), clock=clock, sleep=clock.sleep)

    await limiter.acquire("gemini")
    await limiter.acquire("gemini")
    await limiter.acquire("gemini")  # fills the 3-per-minute window

    await limiter.acquire("gemini")  # must wait for the first call to age out

    assert clock.sleep_calls == [60.0]
    assert clock.now == 60.0


@pytest.mark.asyncio
async def test_a_call_after_the_window_ages_out_never_waits():
    clock = _FakeClock()
    limiter = AIRateLimiter(settings=_settings(), clock=clock, sleep=clock.sleep)

    await limiter.acquire("gemini")
    await limiter.acquire("gemini")
    await limiter.acquire("gemini")

    clock.now += 61  # the whole window has aged out
    await limiter.acquire("gemini")

    assert clock.sleep_calls == []


@pytest.mark.asyncio
async def test_unlimited_provider_never_waits():
    clock = _FakeClock()
    limiter = AIRateLimiter(settings=_settings(), clock=clock, sleep=clock.sleep)

    for _ in range(10):
        await limiter.acquire("openai")

    assert clock.sleep_calls == []


@pytest.mark.asyncio
async def test_unknown_provider_is_treated_as_unlimited():
    clock = _FakeClock()
    limiter = AIRateLimiter(settings=_settings(), clock=clock, sleep=clock.sleep)

    for _ in range(10):
        await limiter.acquire("some-future-provider")

    assert clock.sleep_calls == []


@pytest.mark.asyncio
async def test_providers_have_independent_windows():
    clock = _FakeClock()
    limiter = AIRateLimiter(
        settings=_settings(ai_rate_limit_rpm_gemini=1, ai_rate_limit_rpm_openai=1),
        clock=clock,
        sleep=clock.sleep,
    )

    await limiter.acquire("gemini")  # fills gemini's window
    await limiter.acquire("openai")  # openai's own window is still empty

    assert clock.sleep_calls == []
