"""
Contact API router.

Architecture Freeze v5.0
"""

from __future__ import annotations

from fastapi import APIRouter
from fastapi import status

from app.application.contact.contact_commands import DeleteContactCommand
from app.application.contact.contact_mapper import ContactMapper
from app.application.contact.contact_queries import (
    GetContactQuery,
    ListContactsQuery,
    SearchContactsQuery,
)
from app.application.contact.dto.contact_requests import (
    CreateContactRequestDTO,
    UpdateContactRequestDTO,
)
from app.application.contact.dto.contact_responses import ContactResponseDTO
from app.presentation.api.dependencies.handlers import (
    CreateContactHandlerDependency,
    DeleteContactHandlerDependency,
    GetContactHandlerDependency,
    ListContactHandlerDependency,
    SearchContactHandlerDependency,
    UpdateContactHandlerDependency,
)
from app.presentation.api.dependencies.handlers import get_contact_mapper
from fastapi import Depends


router = APIRouter(
    prefix="/contacts",
    tags=["Contacts"],
)


@router.post(
    "",
    response_model=ContactResponseDTO,
    status_code=status.HTTP_201_CREATED,
)
async def create_contact(
    request: CreateContactRequestDTO,
    handler: CreateContactHandlerDependency,
    mapper: ContactMapper = Depends(get_contact_mapper),
) -> ContactResponseDTO:
    """Create a Contact."""
    command = mapper.to_create_command(request)
    return await handler.handle(command)


@router.get(
    "",
    response_model=list[ContactResponseDTO],
)
async def list_contacts(
    handler: ListContactHandlerDependency,
    skip: int = 0,
    limit: int = 100,
) -> list[ContactResponseDTO]:
    """List Contacts."""
    query = ListContactsQuery(
        skip=skip,
        limit=limit,
    )
    return await handler.handle(query)


@router.get(
    "/search",
    response_model=list[ContactResponseDTO],
)
async def search_contacts(
    search_text: str,
    handler: SearchContactHandlerDependency,
    skip: int = 0,
    limit: int = 100,
) -> list[ContactResponseDTO]:
    """Search Contacts."""
    query = SearchContactsQuery(
        search_text=search_text,
        skip=skip,
        limit=limit,
    )
    return await handler.handle(query)


@router.get(
    "/{contact_id}",
    response_model=ContactResponseDTO,
)
async def get_contact(
    contact_id: str,
    handler: GetContactHandlerDependency,
) -> ContactResponseDTO:
    """Get a Contact by id."""
    query = GetContactQuery(contact_id=contact_id)
    return await handler.handle(query)


@router.put(
    "/{contact_id}",
    response_model=ContactResponseDTO,
)
async def update_contact(
    contact_id: str,
    request: UpdateContactRequestDTO,
    handler: UpdateContactHandlerDependency,
    mapper: ContactMapper = Depends(get_contact_mapper),
) -> ContactResponseDTO:
    """Update a Contact."""
    command = mapper.to_update_command(
        request=request,
        contact_id=contact_id,
    )
    return await handler.handle(command)


@router.delete(
    "/{contact_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_contact(
    contact_id: str,
    handler: DeleteContactHandlerDependency,
) -> None:
    """Delete a Contact."""
    command = DeleteContactCommand(contact_id=contact_id)
    await handler.handle(command)
