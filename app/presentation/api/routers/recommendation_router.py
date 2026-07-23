from fastapi import APIRouter, status

from app.application.recommendation.commands.generate_recommendation.generate_recommendation_command import (
    GenerateRecommendationCommand,
)
from app.presentation.api.dependencies.mediator import MediatorDependency
from app.presentation.common.response import ApiResponse
from app.presentation.schemas.requests.recommendation_request import (
    GenerateRecommendationRequest,
)
from app.presentation.schemas.responses.recommendation_response import (
    RecommendationResponse,
)

router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendation"],
)


@router.post(
    "",
    response_model=ApiResponse[RecommendationResponse],
    status_code=status.HTTP_200_OK,
)
async def generate_recommendation(
    request: GenerateRecommendationRequest,
    mediator: MediatorDependency,
) -> ApiResponse[RecommendationResponse]:

    command = GenerateRecommendationCommand(
        assessment_id=request.assessment_id,
    )

    result = await mediator.send(command)

    return ApiResponse(
        success=True,
        message="Recommendation generated successfully.",
        data=RecommendationResponse.model_validate(result),
    )