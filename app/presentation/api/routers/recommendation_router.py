from uuid import UUID

from fastapi import APIRouter, status

from app.application.recommendation.commands.create_recommendation.create_recommendation_command import (
    CreateRecommendationCommand,
)
from app.application.recommendation.queries.get_recommendation_by_id import (
    GetRecommendationByIdQuery,
)
from app.presentation.api.dependencies.mediator import (
    MediatorDependency,
)
from app.presentation.common.response import (
    ApiResponse,
)
from app.presentation.schemas.requests.recommendation_request import (
    CreateRecommendationRequest,
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
    status_code=status.HTTP_201_CREATED,
)
async def create_recommendation(
    request: CreateRecommendationRequest,
    mediator: MediatorDependency,
) -> ApiResponse[RecommendationResponse]:

    command = CreateRecommendationCommand(
        assessment_id=request.assessment_id,
    )

    result = await mediator.send(
        command,
    )

    return ApiResponse(
        success=True,
        message="Recommendation created successfully.",
        data=RecommendationResponse.model_validate(
            result,
        ),
    )


@router.get(
    "/{recommendation_id}",
    response_model=ApiResponse[RecommendationResponse],
    status_code=status.HTTP_200_OK,
)
async def get_recommendation(
    recommendation_id: UUID,
    mediator: MediatorDependency,
) -> ApiResponse[RecommendationResponse]:

    query = GetRecommendationByIdQuery(
        recommendation_id=recommendation_id,
    )

    result = await mediator.send(
        query,
    )

    return ApiResponse(
        success=True,
        message="Recommendation retrieved successfully.",
        data=RecommendationResponse.model_validate(
            result,
        ),
    )