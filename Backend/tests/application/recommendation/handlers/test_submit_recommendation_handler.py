"""
Tests for SubmitRecommendationHandler.

Regression guard: this handler existed as real code but was never wired
into any router endpoint, and its original constructor shape
(repository, validator, mapper) didn't match how DI actually wires
handlers anywhere else in this codebase -- it's been rewritten to the
unit_of_work pattern every other modern handler uses (see
GetRecommendationHandler) as part of finally reaching it from
POST /recommendations/{id}/submit.
"""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from app.application.common.exceptions.conflict_exception import ConflictException
from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.recommendation.commands.submit_recommendation import (
    SubmitRecommendationCommand,
)
from app.application.recommendation.handlers.submit_recommendation_handler import (
    SubmitRecommendationHandler,
)
from app.domain.assessment.identifiers.assessment_id import AssessmentId
from app.domain.recommendation.entities.recommendation import Recommendation
from app.domain.recommendation.entities.solution import Solution
from app.domain.recommendation.enums.recommendation_status import RecommendationStatus


def _recommendation_with_a_solution() -> Recommendation:
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
    return recommendation


@pytest.fixture
def unit_of_work():
    uow = AsyncMock()
    uow.__aenter__.return_value = uow
    uow.__aexit__.return_value = False
    return uow


@pytest.fixture
def handler(unit_of_work):
    return SubmitRecommendationHandler(unit_of_work=unit_of_work)


@pytest.mark.asyncio
async def test_submit_moves_a_draft_recommendation_with_solutions_to_under_review(handler, unit_of_work):
    recommendation = _recommendation_with_a_solution()
    unit_of_work.recommendation_repository.get_by_id.return_value = recommendation

    result = await handler.handle(SubmitRecommendationCommand(recommendation_id=recommendation.id.value))

    assert result.status == RecommendationStatus.UNDER_REVIEW.value
    unit_of_work.recommendation_repository.update.assert_awaited_once()


@pytest.mark.asyncio
async def test_submit_raises_not_found_for_an_unknown_recommendation(handler, unit_of_work):
    unit_of_work.recommendation_repository.get_by_id.return_value = None

    with pytest.raises(NotFoundException):
        await handler.handle(SubmitRecommendationCommand(recommendation_id=AssessmentId().value))


@pytest.mark.asyncio
async def test_submit_raises_conflict_for_a_recommendation_with_no_solutions(handler, unit_of_work):
    recommendation = Recommendation(assessment_id=AssessmentId())
    unit_of_work.recommendation_repository.get_by_id.return_value = recommendation

    with pytest.raises(ConflictException):
        await handler.handle(SubmitRecommendationCommand(recommendation_id=recommendation.id.value))

    unit_of_work.recommendation_repository.update.assert_not_awaited()
