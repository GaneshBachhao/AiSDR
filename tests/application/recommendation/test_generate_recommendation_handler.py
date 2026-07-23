from uuid import uuid4
from unittest.mock import AsyncMock

import pytest

from app.application.common.handler.handler_context import (
    HandlerContext,
)
from app.application.recommendation.commands.generate_recommendation import (
    GenerateRecommendationCommand,
)
from app.application.recommendation.handlers.generate_recommendation_handler import (
    GenerateRecommendationHandler,
)
from app.domain.assessment.entities.assessment import (
    Assessment,
)
from app.domain.assessment.identifiers.assessment_id import (
    AssessmentId,
)
from app.domain.discovery.identifiers.discovery_session_id import (
    DiscoverySessionId,
)
from app.domain.recommendation.entities.recommendation import (
    Recommendation,
)


@pytest.mark.asyncio
async def test_returns_failure_when_assessment_missing():
    assessment_repo = AsyncMock()
    recommendation_repo = AsyncMock()

    assessment_repo.get_by_id.return_value = None

    handler = GenerateRecommendationHandler(
        assessment_repo,
        recommendation_repo,
    )

    command = GenerateRecommendationCommand(
        assessment_id=uuid4(),
    )

    result = await handler.execute(
        command,
        HandlerContext(),
    )

    assert not result.success


@pytest.mark.asyncio
async def test_returns_existing_recommendation():
    assessment = Assessment(
        discovery_session_id=DiscoverySessionId(),
    )

    recommendation = Recommendation(
        assessment_id=assessment.id,
    )

    assessment_repo = AsyncMock()
    recommendation_repo = AsyncMock()

    assessment_repo.get_by_id.return_value = assessment

    recommendation_repo.get_by_assessment.return_value = (
        recommendation
    )

    handler = GenerateRecommendationHandler(
        assessment_repo,
        recommendation_repo,
    )

    command = GenerateRecommendationCommand(
        assessment_id=assessment.id.value,
    )

    result = await handler.execute(
        command,
        HandlerContext(),
    )

    assert result.success

    assert result.data.id == recommendation.id.value


@pytest.mark.asyncio
async def test_creates_new_recommendation():
    assessment = Assessment(
        discovery_session_id=DiscoverySessionId(),
    )

    assessment_repo = AsyncMock()
    recommendation_repo = AsyncMock()

    assessment_repo.get_by_id.return_value = assessment

    recommendation_repo.get_by_assessment.return_value = None

    recommendation_repo.save.side_effect = (
        lambda recommendation: recommendation
    )

    handler = GenerateRecommendationHandler(
        assessment_repo,
        recommendation_repo,
    )

    command = GenerateRecommendationCommand(
        assessment_id=assessment.id.value,
    )

    result = await handler.execute(
        command,
        HandlerContext(),
    )

    assert result.success

    recommendation_repo.save.assert_awaited_once()