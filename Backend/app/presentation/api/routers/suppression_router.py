"""
Suppression API router (EPIC-11).

Internal ops action -- gated behind the blanket auth gate like every
other router, not public (contrast with webhook_router.py, which is a
third-party callback with its own shared-secret auth instead).
"""

from __future__ import annotations

from fastapi import APIRouter, Query, Response, status

from app.application.suppression.dto.suppression_requests import (
    CreateSuppressionRequestDTO,
)
from app.application.suppression.dto.suppression_responses import (
    SuppressionCheckResponseDTO,
    SuppressionEntryResponseDTO,
)
from app.application.suppression.suppression_commands import DeleteSuppressionCommand
from app.application.suppression.suppression_mapper import SuppressionMapper
from app.presentation.api.dependencies.handlers import (
    CheckSuppressionHandlerDependency,
    CreateSuppressionHandlerDependency,
    DeleteSuppressionHandlerDependency,
    ListSuppressionsHandlerDependency,
)

router = APIRouter(
    prefix="/suppressions",
    tags=["Suppressions"],
)


@router.post(
    "",
    response_model=SuppressionEntryResponseDTO,
)
async def create_suppression(
    request: CreateSuppressionRequestDTO,
    handler: CreateSuppressionHandlerDependency,
) -> SuppressionEntryResponseDTO:
    """Manually add an email to the do-not-contact list."""
    return await handler.handle(SuppressionMapper.to_create_command(request))


@router.get(
    "",
    response_model=list[SuppressionEntryResponseDTO],
)
async def list_suppressions(
    handler: ListSuppressionsHandlerDependency,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
) -> list[SuppressionEntryResponseDTO]:
    """List all suppression entries."""
    return await handler.handle(skip=skip, limit=limit)


@router.get(
    "/check",
    response_model=SuppressionCheckResponseDTO,
)
async def check_suppression(
    handler: CheckSuppressionHandlerDependency,
    email: str = Query(...),
) -> SuppressionCheckResponseDTO:
    """Check whether a single email address is currently suppressed."""
    return await handler.handle(email)


@router.delete(
    "/{suppression_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_suppression(
    suppression_id: str,
    handler: DeleteSuppressionHandlerDependency,
) -> Response:
    """Lift a suppression."""
    await handler.handle(DeleteSuppressionCommand(suppression_id=suppression_id))
    return Response(status_code=status.HTTP_204_NO_CONTENT)
