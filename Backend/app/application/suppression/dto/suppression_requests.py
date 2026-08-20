"""Suppression request DTOs."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.suppression.enums.suppression_reason import SuppressionReason


@dataclass(slots=True)
class CreateSuppressionRequestDTO:
    """Request to manually add an email to the do-not-contact list."""

    email: str
    reason: SuppressionReason = SuppressionReason.MANUAL
    notes: str | None = None


@dataclass(slots=True)
class RecordEmailEventRequestDTO:
    """Provider-agnostic bounce/complaint webhook payload.

    Deliberately not shaped after any specific ESP's real webhook schema
    (SendGrid/Mailgun/SES/...) -- this app doesn't integrate a real one
    yet, so matching one vendor's exact contract now would be guessing.
    A future real integration adapter translates its provider's payload
    into this shape.
    """

    email: str
    event_type: str
    reason: str | None = None
    occurred_at: str | None = None
