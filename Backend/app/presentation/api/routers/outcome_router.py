"""
Outcome API router (EPIC-12).

Internal CRM action -- gated behind the blanket auth gate like every
other router, same tier as suppression_router.py.
"""

from __future__ import annotations

from fastapi import APIRouter, Query, Response, status

from app.application.outcome.dto.outcome_requests import (
    CreateOutcomeEventRequestDTO,
)
from app.application.outcome.dto.outcome_responses import (
    OutcomeEventResponseDTO,
)
from app.application.outcome.outcome_commands import DeleteOutcomeEventCommand
from app.application.outcome.outcome_mapper import OutcomeMapper
from app.presentation.api.dependencies.handlers import (
    CreateOutcomeEventHandlerDependency,
    DeleteOutcomeEventHandlerDependency,
    ListOutcomeEventsHandlerDependency,
)

router = APIRouter(
    prefix="/outcomes",
    tags=["Outcomes"],
)


@router.post(
    "",
    response_model=OutcomeEventResponseDTO,
    status_code=status.HTTP_201_CREATED,
)
async def create_outcome_event(
    request: CreateOutcomeEventRequestDTO,
    handler: CreateOutcomeEventHandlerDependency,
) -> OutcomeEventResponseDTO:
    """Record an outcome for a Lead."""
    return await handler.handle(OutcomeMapper.to_create_command(request))


@router.get(
    "",
    response_model=list[OutcomeEventResponseDTO],
)
async def list_outcome_events(
    handler: ListOutcomeEventsHandlerDependency,
    lead_id: str | None = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
) -> list[OutcomeEventResponseDTO]:
    """List outcome events, optionally filtered to one Lead."""
    return await handler.handle(lead_id=lead_id, skip=skip, limit=limit)


@router.delete(
    "/{outcome_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_outcome_event(
    outcome_id: str,
    handler: DeleteOutcomeEventHandlerDependency,
) -> Response:
    """Remove a mis-logged outcome."""
    await handler.handle(DeleteOutcomeEventCommand(outcome_id=outcome_id))
    return Response(status_code=status.HTTP_204_NO_CONTENT)
