"""Tests for verify_webhook_secret (EPIC-11)."""

from __future__ import annotations

import pytest

from app.application.common.exceptions.unauthorized_exception import (
    UnauthorizedException,
)
from app.infrastructure.configuration.webhook_settings import WebhookSettings
from app.presentation.api.dependencies.webhooks import verify_webhook_secret


@pytest.mark.asyncio
async def test_matching_secret_passes() -> None:
    settings = WebhookSettings(email_webhook_secret="real-secret")

    await verify_webhook_secret(x_webhook_secret="real-secret", settings=settings)


@pytest.mark.asyncio
async def test_wrong_secret_raises() -> None:
    settings = WebhookSettings(email_webhook_secret="real-secret")

    with pytest.raises(UnauthorizedException):
        await verify_webhook_secret(x_webhook_secret="wrong-secret", settings=settings)


@pytest.mark.asyncio
async def test_missing_header_raises() -> None:
    settings = WebhookSettings(email_webhook_secret="real-secret")

    with pytest.raises(UnauthorizedException):
        await verify_webhook_secret(x_webhook_secret=None, settings=settings)


@pytest.mark.asyncio
async def test_unconfigured_secret_fails_closed_even_with_a_blank_header() -> None:
    """A blank configured secret must never mean "no auth required" --
    every request is rejected, including one that (perhaps accidentally)
    sends a blank header too."""
    settings = WebhookSettings(email_webhook_secret="")

    with pytest.raises(UnauthorizedException):
        await verify_webhook_secret(x_webhook_secret="", settings=settings)
