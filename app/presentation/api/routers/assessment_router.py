from fastapi import APIRouter, status

from app.application.assessment.commands.create_assessment.create_assessment_command import (
    CreateAssessmentCommand,
)
from app.presentation.api.dependencies.mediator import MediatorDependency
from app.presentation.common.response import ApiResponse
from app.presentation.schemas.requests.assessment_request import (
    CreateAssessmentRequest,
)
from app.presentation.schemas.responses.assessment_response import (
    AssessmentResponse,
)

router = APIRouter(
    prefix="/assessments",
    tags=["Assessment"],
)


@router.post(
    "",
    response_model=ApiResponse[AssessmentResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_assessment(
    request: CreateAssessmentRequest,
    mediator: MediatorDependency,
) -> ApiResponse[AssessmentResponse]:

    command = CreateAssessmentCommand(
        discovery_id=request.discovery_id,
    )

    result = await mediator.send(command)

    return ApiResponse(
        success=True,
        message="Assessment completed successfully.",
        data=AssessmentResponse.model_validate(result),
    )