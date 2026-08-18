"""
Lead API router.

Architecture Freeze v5.0
"""

from __future__ import annotations

from fastapi import APIRouter, Query, Response, status

from app.application.lead.dto.lead_requests import (
    CreateLeadRequestDTO,
    UpdateLeadRequestDTO,
)
from app.application.lead.dto.lead_responses import LeadResponseDTO
from app.application.lead.lead_commands import DeleteLeadCommand
from app.application.lead.lead_mapper import LeadMapper
from app.application.lead.lead_queries import (
    GetLeadQuery,
    ListLeadQuery,
    SearchLeadQuery,
)
from app.presentation.api.dependencies.handlers import (
    CreateLeadHandlerDependency,
    DeleteLeadHandlerDependency,
    GetLeadHandlerDependency,
    ListLeadHandlerDependency,
    SearchLeadHandlerDependency,
    UpdateLeadHandlerDependency,
)

router = APIRouter(
    prefix="/leads",
    tags=["Leads"],
)


@router.post(
    "",
    response_model=LeadResponseDTO,
    status_code=status.HTTP_201_CREATED,
)
async def create_lead(
    request: CreateLeadRequestDTO,
    handler: CreateLeadHandlerDependency,
) -> LeadResponseDTO:
    """Create a Lead."""
    return await handler.handle(
        LeadMapper.to_create_command(request),
    )


@router.get(
    "",
    response_model=list[LeadResponseDTO],
)
async def list_leads(
    handler: ListLeadHandlerDependency,
    company_id: str | None = Query(default=None),
    contact_id: str | None = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
) -> list[LeadResponseDTO]:
    """List Leads."""
    return await handler.handle(
        ListLeadQuery(
            company_id=company_id,
            contact_id=contact_id,
            skip=skip,
            limit=limit,
        )
    )


@router.get(
    "/search",
    response_model=list[LeadResponseDTO],
)
async def search_leads(
    handler: SearchLeadHandlerDependency,
    keyword: str = Query(..., min_length=1),
    company_id: str | None = Query(default=None),
    contact_id: str | None = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
) -> list[LeadResponseDTO]:
    """Search Leads."""
    return await handler.handle(
        SearchLeadQuery(
            search_term=keyword,
            company_id=company_id,
            contact_id=contact_id,
            skip=skip,
            limit=limit,
        )
    )


@router.get(
    "/{lead_id}",
    response_model=LeadResponseDTO,
)
async def get_lead(
    lead_id: str,
    handler: GetLeadHandlerDependency,
) -> LeadResponseDTO:
    """Get a Lead by ID."""
    return await handler.handle(
        GetLeadQuery(lead_id=lead_id),
    )


@router.put(
    "/{lead_id}",
    response_model=LeadResponseDTO,
)
async def update_lead(
    lead_id: str,
    request: UpdateLeadRequestDTO,
    handler: UpdateLeadHandlerDependency,
) -> LeadResponseDTO:
    """Update a Lead."""
    return await handler.handle(
        LeadMapper.to_update_command(request, lead_id),
    )


@router.delete(
    "/{lead_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_lead(
    lead_id: str,
    handler: DeleteLeadHandlerDependency,
) -> Response:
    """Delete a Lead."""
    await handler.handle(
        DeleteLeadCommand(lead_id=lead_id),
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
