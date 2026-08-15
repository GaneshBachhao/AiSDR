"""
Discovery API Router.

Architecture Freeze v5.0
"""

from __future__ import annotations

from fastapi import APIRouter, Query, Response, status

from app.application.discovery.discovery_mapper import DiscoveryMapper
from app.application.discovery.discovery_queries import (
    GetDiscoveryQuery,
    ListDiscoveryQuery,
    SearchDiscoveryQuery,
)
from app.application.discovery.dto.discovery_requests import (
    CreateDiscoveryRequestDTO,
    UpdateDiscoveryRequestDTO,
)
from app.application.discovery.dto.discovery_responses import DiscoveryResponseDTO
from app.presentation.api.dependencies.handlers import (
    CreateDiscoveryHandlerDependency,
    DeleteDiscoveryHandlerDependency,
    GetDiscoveryHandlerDependency,
    ListDiscoveryHandlerDependency,
    SearchDiscoveryHandlerDependency,
    UpdateDiscoveryHandlerDependency,
)

router = APIRouter(prefix="/discoveries", tags=["Discoveries"])


@router.post(
    "",
    response_model=DiscoveryResponseDTO,
    status_code=status.HTTP_201_CREATED,
)
async def create_discovery(
    request: CreateDiscoveryRequestDTO,
    handler: CreateDiscoveryHandlerDependency,
) -> DiscoveryResponseDTO:
    """Create a discovery session for a lead."""
    return await handler.handle(DiscoveryMapper.to_create_command(request))


@router.get("", response_model=list[DiscoveryResponseDTO])
async def list_discoveries(
    handler: ListDiscoveryHandlerDependency,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
) -> list[DiscoveryResponseDTO]:
    """List discovery sessions."""
    return await handler.handle(ListDiscoveryQuery(skip=skip, limit=limit))


@router.get("/search", response_model=list[DiscoveryResponseDTO])
async def search_discoveries(
    search_text: str,
    handler: SearchDiscoveryHandlerDependency,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
) -> list[DiscoveryResponseDTO]:
    """Search discovery text fields."""
    return await handler.handle(
        SearchDiscoveryQuery(
            search_text=search_text,
            skip=skip,
            limit=limit,
        )
    )


@router.get("/{discovery_id}", response_model=DiscoveryResponseDTO)
async def get_discovery(
    discovery_id: str,
    handler: GetDiscoveryHandlerDependency,
) -> DiscoveryResponseDTO:
    """Get a discovery by id."""
    return await handler.handle(GetDiscoveryQuery(discovery_id=discovery_id))


@router.put("/{discovery_id}", response_model=DiscoveryResponseDTO)
async def update_discovery(
    discovery_id: str,
    request: UpdateDiscoveryRequestDTO,
    handler: UpdateDiscoveryHandlerDependency,
) -> DiscoveryResponseDTO:
    """Update a discovery session."""
    return await handler.handle(
        DiscoveryMapper.to_update_command(discovery_id, request)
    )


@router.delete(
    "/{discovery_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_discovery(
    discovery_id: str,
    handler: DeleteDiscoveryHandlerDependency,
) -> Response:
    """Delete a discovery session."""
    await handler.handle(
        DiscoveryMapper.to_delete_command(discovery_id),
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
