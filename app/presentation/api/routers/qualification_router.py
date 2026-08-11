"""Qualification API router."""

from __future__ import annotations

from fastapi import APIRouter, Query, Response, status

from app.application.qualification.dto.qualification_request import (
    CreateQualificationRequestDTO,
    UpdateQualificationRequestDTO,
)
from app.application.qualification.handlers.create_qualification_handler import CreateQualificationHandler
from app.application.qualification.handlers.delete_qualification_handler import DeleteQualificationHandler
from app.application.qualification.handlers.get_qualification_handler import GetQualificationHandler
from app.application.qualification.handlers.list_qualification_handler import ListQualificationHandler
from app.application.qualification.handlers.update_qualification_handler import UpdateQualificationHandler
from app.application.qualification.qualification_commands import (
    CreateQualificationCommand,
    DeleteQualificationCommand,
    UpdateQualificationCommand,
)
from app.application.qualification.qualification_queries import (
    GetQualificationQuery,
    ListQualificationsQuery,
)
from app.presentation.api.dependencies.handlers import (
    CreateQualificationHandlerDependency,
    DeleteQualificationHandlerDependency,
    GetQualificationHandlerDependency,
    ListQualificationHandlerDependency,
    UpdateQualificationHandlerDependency,
)


router = APIRouter(
    prefix="/qualifications",
    tags=["Qualifications"],
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def create_qualification(
    request: CreateQualificationRequestDTO,
    handler: CreateQualificationHandlerDependency,
):
    command = CreateQualificationCommand(**request.model_dump())
    return await handler.handle(command)


@router.get(
    "/{qualification_id}",
)
async def get_qualification(
    qualification_id: str,
    handler: GetQualificationHandlerDependency,
):
    query = GetQualificationQuery(
        qualification_id=qualification_id,
    )
    return await handler.handle(query)


@router.get(
    "",
)
async def list_qualifications(
    handler: ListQualificationHandlerDependency,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    lead_id: str | None = Query(default=None),
    assessment_id: str | None = Query(default=None),
):
    query = ListQualificationsQuery(
        page=(skip // limit) + 1,
        page_size=limit,
        lead_id=lead_id,
        assessment_id=assessment_id,
    )
    return await handler.handle(query)


@router.put(
    "/{qualification_id}",
)
async def update_qualification(
    qualification_id: str,
    request: UpdateQualificationRequestDTO,
    handler: UpdateQualificationHandlerDependency,
):
    command = UpdateQualificationCommand(
        qualification_id=qualification_id,
        **request.model_dump(exclude_unset=True),
    )
    return await handler.handle(command)


@router.delete(
    "/{qualification_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_qualification(
    qualification_id: str,
    handler: DeleteQualificationHandlerDependency,
):
    command = DeleteQualificationCommand(
        qualification_id=qualification_id,
    )
    await handler.handle(command)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
