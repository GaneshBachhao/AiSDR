"""
Tests for RejectRecommendationHandler.

Fills a real, previously-unwired gap: Recommendation.reject() already
existed as a working domain method, but nothing exposed it through the
application/presentation layers -- unlike approve()/submit(). Mirrors
ApproveRecommendationHandler's shape exactly. Unlike approve(), reject()
has no status guard clause in the domain today (callable from any status),
so there is no "conflict" test case here -- that's the real, current
behavior, not an oversight in this handler.
"""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.recommendation.commands.reject_recommendation import (
    RejectRecommendationCommand,
)
from app.application.recommendation.handlers.reject_recommendation_handler import (
    RejectRecommendationHandler,
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
    return RejectRecommendationHandler(unit_of_work=unit_of_work)


@pytest.mark.asyncio
async def test_reject_moves_an_under_review_recommendation_to_rejected(handler, unit_of_work):
    recommendation = _recommendation_under_review()
    unit_of_work.recommendation_repository.get_by_id.return_value = recommendation

    result = await handler.handle(RejectRecommendationCommand(recommendation_id=recommendation.id.value))

    assert result.status == RecommendationStatus.REJECTED.value
    unit_of_work.recommendation_repository.update.assert_awaited_once()


@pytest.mark.asyncio
async def test_reject_works_from_draft_status_too(handler, unit_of_work):
    recommendation = Recommendation(assessment_id=AssessmentId())
    unit_of_work.recommendation_repository.get_by_id.return_value = recommendation

    result = await handler.handle(RejectRecommendationCommand(recommendation_id=recommendation.id.value))

    assert result.status == RecommendationStatus.REJECTED.value


@pytest.mark.asyncio
async def test_reject_raises_not_found_for_an_unknown_recommendation(handler, unit_of_work):
    unit_of_work.recommendation_repository.get_by_id.return_value = None

    with pytest.raises(NotFoundException):
        await handler.handle(RejectRecommendationCommand(recommendation_id=AssessmentId().value))

    unit_of_work.recommendation_repository.update.assert_not_awaited()
