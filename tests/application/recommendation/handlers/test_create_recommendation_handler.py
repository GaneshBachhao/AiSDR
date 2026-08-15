from __future__ import annotations

import json
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.recommendation.commands.create_recommendation import (
    CreateRecommendationCommand,
)
from app.application.recommendation.handlers.create_recommendation_handler import (
    CreateRecommendationHandler,
)
from app.domain.ai.entities.ai_response import AIResponse
from app.domain.ai.enums.finish_reason import FinishReason
from app.domain.assessment.entities.assessment import Assessment
from app.domain.assessment.identifiers.assessment_id import AssessmentId
from app.domain.discovery.identifiers.discovery_id import DiscoveryId
from app.domain.recommendation.entities.recommendation import Recommendation


def _assessment(**overrides) -> Assessment:
    defaults = dict(
        discovery_id=DiscoveryId(),
        summary="The company relies on manual spreadsheets for reporting.",
        strengths="Strong domain expertise",
        weaknesses="No integration between systems",
        opportunities_summary="Automating monthly reporting",
        risks="Data entry errors",
    )
    defaults.update(overrides)
    return Assessment(**defaults)


def _ai_response(content: str) -> AIResponse:
    return AIResponse(content=content, finish_reason=FinishReason.STOP)


def _fake_uow(assessment=None, existing_recommendation=None):
    uow = AsyncMock()
    uow.assessment_repository.get_by_id.return_value = assessment
    uow.recommendation_repository.get_by_assessment_id.return_value = existing_recommendation
    return uow


@pytest.mark.asyncio
async def test_returns_existing_recommendation_without_calling_ai():
    existing = Recommendation(assessment_id=AssessmentId())
    uow = _fake_uow(existing_recommendation=existing)
    ai_service = AsyncMock()

    handler = CreateRecommendationHandler(uow, ai_service)
    result = await handler.handle(CreateRecommendationCommand(assessment_id=uuid4()))

    assert result.id == existing.id.value
    ai_service.execute.assert_not_awaited()


@pytest.mark.asyncio
async def test_raises_not_found_when_assessment_missing():
    uow = _fake_uow(assessment=None)
    ai_service = AsyncMock()
    handler = CreateRecommendationHandler(uow, ai_service)

    with pytest.raises(NotFoundException):
        await handler.handle(CreateRecommendationCommand(assessment_id=uuid4()))


@pytest.mark.asyncio
async def test_raises_when_assessment_has_no_content():
    empty_assessment = Assessment(discovery_id=DiscoveryId())
    uow = _fake_uow(assessment=empty_assessment)
    ai_service = AsyncMock()
    handler = CreateRecommendationHandler(uow, ai_service)

    with pytest.raises(ValueError, match="no summary/analysis"):
        await handler.handle(CreateRecommendationCommand(assessment_id=uuid4()))

    ai_service.execute.assert_not_awaited()


@pytest.mark.asyncio
async def test_generates_and_persists_solutions_from_ai_response():
    assessment = _assessment()
    uow = _fake_uow(assessment=assessment)
    ai_service = AsyncMock()
    ai_service.execute.return_value = _ai_response(
        json.dumps(
            [
                {
                    "title": "Business Process Automation",
                    "description": "Automate the monthly reporting workflow.",
                    "solution_type": "Automation",
                    "priority": "High",
                    "is_existing_offering": True,
                },
                {
                    "title": "Custom Reporting Dashboard",
                    "description": "A sector-appropriate generic idea.",
                    "solution_type": "Analytics",
                    "priority": "Medium",
                    "is_existing_offering": False,
                },
            ]
        )
    )

    handler = CreateRecommendationHandler(uow, ai_service)
    result = await handler.handle(CreateRecommendationCommand(assessment_id=uuid4()))

    assert len(result.solutions) == 2
    assert result.solutions[0].title == "Business Process Automation"
    assert result.solutions[0].is_existing_offering is True
    assert result.solutions[1].is_existing_offering is False
    uow.recommendation_repository.add.assert_awaited_once()
    uow.commit.assert_awaited()


@pytest.mark.asyncio
async def test_strips_markdown_fences_from_ai_response():
    assessment = _assessment()
    uow = _fake_uow(assessment=assessment)
    ai_service = AsyncMock()
    fenced = "```json\n" + json.dumps(
        [{"title": "AI Consulting", "description": "x", "solution_type": "AI Agent",
          "priority": "Medium", "is_existing_offering": True}]
    ) + "\n```"
    ai_service.execute.return_value = _ai_response(fenced)

    handler = CreateRecommendationHandler(uow, ai_service)
    result = await handler.handle(CreateRecommendationCommand(assessment_id=uuid4()))

    assert len(result.solutions) == 1
    assert result.solutions[0].title == "AI Consulting"


@pytest.mark.asyncio
async def test_raises_on_unparseable_ai_response_instead_of_saving_an_empty_shell():
    assessment = _assessment()
    uow = _fake_uow(assessment=assessment)
    ai_service = AsyncMock()
    ai_service.execute.return_value = _ai_response("not json at all")

    handler = CreateRecommendationHandler(uow, ai_service)

    with pytest.raises(ValueError, match="not valid JSON"):
        await handler.handle(CreateRecommendationCommand(assessment_id=uuid4()))

    uow.recommendation_repository.add.assert_not_awaited()


@pytest.mark.asyncio
async def test_raises_when_ai_returns_an_empty_list():
    assessment = _assessment()
    uow = _fake_uow(assessment=assessment)
    ai_service = AsyncMock()
    ai_service.execute.return_value = _ai_response("[]")

    handler = CreateRecommendationHandler(uow, ai_service)

    with pytest.raises(ValueError, match="did not contain any solutions"):
        await handler.handle(CreateRecommendationCommand(assessment_id=uuid4()))
