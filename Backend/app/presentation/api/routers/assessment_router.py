"""
Assessment API router.
"""

from __future__ import annotations

from fastapi import APIRouter, Query, Response, status

from app.application.assessment.assessment_commands import (
    CompleteAssessmentCommand,
    DeleteAssessmentCommand,
    StartAssessmentCommand,
)
from app.application.assessment.assessment_mapper import AssessmentMapper
from app.application.assessment.assessment_queries import (
    GetAssessmentQuery,
    ListAssessmentsQuery,
)
from app.application.assessment.dto.assessment_request import (
    CompleteAssessmentRequestDTO,
    CreateAssessmentRequestDTO,
    UpdateAssessmentRequestDTO,
)
from app.application.assessment.dto.assessment_response import (
    CreateAssessmentResponseDTO,
    GetAssessmentResponseDTO,
    ListAssessmentResponseDTO,
    UpdateAssessmentResponseDTO,
)
from app.presentation.api.dependencies.handlers import (
    CompleteAssessmentHandlerDependency,
    CreateAssessmentHandlerDependency,
    DeleteAssessmentHandlerDependency,
    GetAssessmentHandlerDependency,
    ListAssessmentHandlerDependency,
    StartAssessmentHandlerDependency,
    UpdateAssessmentHandlerDependency,
)

router = APIRouter(prefix="/assessments", tags=["Assessment"])


@router.post(
    "",
    response_model=CreateAssessmentResponseDTO,
    status_code=status.HTTP_201_CREATED,
)
async def create_assessment(
    request: CreateAssessmentRequestDTO,
    handler: CreateAssessmentHandlerDependency,
) -> CreateAssessmentResponseDTO:
    command = AssessmentMapper.to_create_command(request)
    return await handler.handle(command)


@router.get(
    "",
    response_model=list[ListAssessmentResponseDTO],
)
async def list_assessments(
    handler: ListAssessmentHandlerDependency,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=200),
    discovery_id: str | None = Query(default=None),
) -> list[ListAssessmentResponseDTO]:
    query = ListAssessmentsQuery(
        page=page,
        page_size=page_size,
        discovery_id=discovery_id,
    )
    return await handler.handle(query)


@router.get(
    "/{assessment_id}",
    response_model=GetAssessmentResponseDTO,
)
async def get_assessment(
    assessment_id: str,
    handler: GetAssessmentHandlerDependency,
) -> GetAssessmentResponseDTO:
    return await handler.handle(GetAssessmentQuery(assessment_id=assessment_id))


@router.post(
    "/{assessment_id}/start",
    response_model=GetAssessmentResponseDTO,
)
async def start_assessment(
    assessment_id: str,
    handler: StartAssessmentHandlerDependency,
) -> GetAssessmentResponseDTO:
    return await handler.handle(
        StartAssessmentCommand(assessment_id=assessment_id),
    )


@router.post(
    "/{assessment_id}/complete",
    response_model=GetAssessmentResponseDTO,
)
async def complete_assessment(
    assessment_id: str,
    handler: CompleteAssessmentHandlerDependency,
    request: CompleteAssessmentRequestDTO | None = None,
) -> GetAssessmentResponseDTO:
    return await handler.handle(
        CompleteAssessmentCommand(assessment_id=assessment_id, summary=request.summary if request else None),
    )


@router.put(
    "/{assessment_id}",
    response_model=UpdateAssessmentResponseDTO,
)
async def update_assessment(
    assessment_id: str,
    request: UpdateAssessmentRequestDTO,
    handler: UpdateAssessmentHandlerDependency,
) -> UpdateAssessmentResponseDTO:
    command = AssessmentMapper.to_update_command(
        assessment_id=assessment_id,
        dto=request,
    )
    return await handler.handle(command)


@router.delete(
    "/{assessment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_assessment(
    assessment_id: str,
    handler: DeleteAssessmentHandlerDependency,
) -> Response:
    await handler.handle(DeleteAssessmentCommand(assessment_id=assessment_id))
    return Response(status_code=status.HTTP_204_NO_CONTENT)
