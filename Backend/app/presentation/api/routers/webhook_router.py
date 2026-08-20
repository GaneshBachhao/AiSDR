"""
Webhook API router (EPIC-11).

This app's first webhook endpoint -- mounted un-gated at the composition
root (like /auth/login, /health), since a third-party caller can't carry
a JWT bearer token. Auth is its own shared-secret dependency instead
(verify_webhook_secret), not the blanket JWT gate.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.application.suppression.dto.suppression_requests import (
    RecordEmailEventRequestDTO,
)
from app.application.suppression.dto.suppression_responses import (
    SuppressionEntryResponseDTO,
)
from app.application.suppression.suppression_commands import RecordEmailEventCommand
from app.presentation.api.dependencies.handlers import RecordEmailEventHandlerDependency
from app.presentation.api.dependencies.webhooks import verify_webhook_secret

router = APIRouter(
    prefix="/webhooks",
    tags=["Webhooks"],
    dependencies=[Depends(verify_webhook_secret)],
)


@router.post(
    "/email-events",
    response_model=SuppressionEntryResponseDTO,
)
async def record_email_event(
    request: RecordEmailEventRequestDTO,
    handler: RecordEmailEventHandlerDependency,
) -> SuppressionEntryResponseDTO:
    """Auto-suppress on a bounce/complaint event from an email provider."""
    return await handler.handle(
        RecordEmailEventCommand(
            email=request.email,
            event_type=request.event_type,
            reason=request.reason,
        )
    )
