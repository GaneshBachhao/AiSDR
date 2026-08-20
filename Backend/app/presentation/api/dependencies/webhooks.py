"""
Webhook authentication dependencies.

Third-party webhook callers (a future real email provider's bounce/
complaint webhook) can't carry a JWT bearer token, so these endpoints are
mounted un-gated at the composition root (like /auth/login, /health) and
verify their own shared secret here instead -- this app's first webhook
endpoint, no prior pattern to reuse. Fails closed: an unconfigured
(blank) secret rejects every request rather than accepting everything --
a blank secret must never mean "no auth required."
"""

from __future__ import annotations

import hmac

from fastapi import Depends, Header

from app.application.common.exceptions.unauthorized_exception import (
    UnauthorizedException,
)
from app.infrastructure.configuration.webhook_settings import WebhookSettings

_MISSING_OR_INVALID_SECRET_MESSAGE = "Invalid or missing webhook secret."


def get_webhook_settings() -> WebhookSettings:
    return WebhookSettings()


async def verify_webhook_secret(
    x_webhook_secret: str | None = Header(default=None),
    settings: WebhookSettings = Depends(get_webhook_settings),
) -> None:
    if not settings.email_webhook_secret:
        raise UnauthorizedException(_MISSING_OR_INVALID_SECRET_MESSAGE)

    if x_webhook_secret is None or not hmac.compare_digest(
        x_webhook_secret,
        settings.email_webhook_secret,
    ):
        raise UnauthorizedException(_MISSING_OR_INVALID_SECRET_MESSAGE)
