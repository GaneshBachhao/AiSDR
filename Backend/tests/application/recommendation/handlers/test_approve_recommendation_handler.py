"""
Tests for ApproveRecommendationHandler.

Regression guard: same rewrite as SubmitRecommendationHandler (see that
test file's module docstring) -- this handler also used to have leftover
debug print()/inspect calls dumping repository internals to stdout on
every real call, removed as part of this rewrite.
"""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from app.application.common.exceptions.conflict_exception import ConflictException
from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.recommendation.commands.approve_recommendation import (
    ApproveRecommendationCommand,
)
from app.application.recommendation.handlers.approve_recommendation_handler import (
    ApproveRecommendationHandler,
)
from app.domain.assessment.identifiers.assessment_id import AssessmentId
from app.domain.recommendation.entities.recommendation import Recommendation
from app.domain.recommendation.entities.solution import Solution
from app.domain.recommendation.enums.recommendation_status import RecommendationStatus


def _recommendation_under_review() -> Recommendation:
    recommendation = Recommendation(assessment_id=AssessmentId())
    recommendation.add_solution(
        Solution(
            title="Automate reporting",
            description="Automate the monthly reporting workflow.",
            solution_type="Automation",
            priority="High",
            is_existing_offering=True,
        )
    )
    recommendation.submit()
    return recommendation


@pytest.fixture
def unit_of_work():
    uow = AsyncMock()
    uow.__aenter__.return_value = uow
    uow.__aexit__.return_value = False
    return uow


@pytest.fixture
def handler(unit_of_work):
    return ApproveRecommendationHandler(unit_of_work=unit_of_work)


@pytest.mark.asyncio
async def test_approve_moves_an_under_review_recommendation_to_approved(handler, unit_of_work):
    recommendation = _recommendation_under_review()
    unit_of_work.recommendation_repository.get_by_id.return_value = recommendation

    result = await handler.handle(ApproveRecommendationCommand(recommendation_id=recommendation.id.value))

    assert result.status == RecommendationStatus.APPROVED.value
    unit_of_work.recommendation_repository.update.assert_awaited_once()


@pytest.mark.asyncio
async def test_approve_raises_not_found_for_an_unknown_recommendation(handler, unit_of_work):
    unit_of_work.recommendation_repository.get_by_id.return_value = None

    with pytest.raises(NotFoundException):
        await handler.handle(ApproveRecommendationCommand(recommendation_id=AssessmentId().value))


@pytest.mark.asyncio
async def test_approve_raises_conflict_for_a_recommendation_still_in_draft(handler, unit_of_work):
    recommendation = Recommendation(assessment_id=AssessmentId())
    unit_of_work.recommendation_repository.get_by_id.return_value = recommendation

    with pytest.raises(ConflictException):
        await handler.handle(ApproveRecommendationCommand(recommendation_id=recommendation.id.value))

    unit_of_work.recommendation_repository.update.assert_not_awaited()
