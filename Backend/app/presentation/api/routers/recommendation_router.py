"""Recommendation API router."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Query, status

from app.application.recommendation.commands.approve_recommendation import ApproveRecommendationCommand
from app.application.recommendation.commands.create_recommendation import CreateRecommendationCommand
from app.application.recommendation.commands.reject_recommendation import RejectRecommendationCommand
from app.application.recommendation.commands.submit_recommendation import SubmitRecommendationCommand
from app.application.recommendation.dto.recommendation_dto import RecommendationDTO
from app.application.recommendation.queries.get_recommendation_by_id import GetRecommendationByIdQuery
from app.application.recommendation.queries.list_recommendations import ListRecommendationsQuery
from app.presentation.api.dependencies.handlers import (
    ApproveRecommendationHandlerDependency,
    CreateRecommendationHandlerDependency,
    GetRecommendationHandlerDependency,
    ListRecommendationHandlerDependency,
    RejectRecommendationHandlerDependency,
    SubmitRecommendationHandlerDependency,
)
from app.presentation.schemas.requests.recommendation_request import GenerateRecommendationRequest

router = APIRouter(prefix="/recommendations", tags=["Recommendation"])


@router.post(
    "",
    response_model=RecommendationDTO,
    status_code=status.HTTP_201_CREATED,
)
async def create_recommendation(
    request: GenerateRecommendationRequest,
    handler: CreateRecommendationHandlerDependency,
) -> RecommendationDTO:
    return await handler.handle(
        CreateRecommendationCommand(assessment_id=request.assessment_id),
    )


@router.get(
    "",
    response_model=list[RecommendationDTO],
)
async def list_recommendations(
    handler: ListRecommendationHandlerDependency,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=200),
) -> list[RecommendationDTO]:
    return await handler.handle(
        ListRecommendationsQuery(page=page, page_size=page_size),
    )


@router.get(
    "/{recommendation_id}",
    response_model=RecommendationDTO,
)
async def get_recommendation(
    recommendation_id: str,
    handler: GetRecommendationHandlerDependency,
) -> RecommendationDTO:
    return await handler.handle(
        GetRecommendationByIdQuery(recommendation_id=UUID(recommendation_id)),
    )


@router.post(
    "/{recommendation_id}/submit",
    response_model=RecommendationDTO,
)
async def submit_recommendation(
    recommendation_id: str,
    handler: SubmitRecommendationHandlerDependency,
) -> RecommendationDTO:
    return await handler.handle(
        SubmitRecommendationCommand(recommendation_id=UUID(recommendation_id)),
    )


@router.post(
    "/{recommendation_id}/approve",
    response_model=RecommendationDTO,
)
async def approve_recommendation(
    recommendation_id: str,
    handler: ApproveRecommendationHandlerDependency,
) -> RecommendationDTO:
    return await handler.handle(
        ApproveRecommendationCommand(recommendation_id=UUID(recommendation_id)),
    )


@router.post(
    "/{recommendation_id}/reject",
    response_model=RecommendationDTO,
)
async def reject_recommendation(
    recommendation_id: str,
    handler: RejectRecommendationHandlerDependency,
) -> RecommendationDTO:
    return await handler.handle(
        RejectRecommendationCommand(recommendation_id=UUID(recommendation_id)),
    )
