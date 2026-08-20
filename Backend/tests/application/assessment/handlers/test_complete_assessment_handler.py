"""
Tests for CompleteAssessmentHandler.

Regression coverage for a real, previously-unfixed gap: `complete_assessment_
handler.py` existed as a completely empty file with zero references, so
Assessment.complete() (stamps completed_at, sets status=COMPLETED) had no
route wired to it at all -- completion was only reachable indirectly through
the generic PUT update endpoint, which never called complete() and so never
stamped completed_at correctly.
"""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from app.application.assessment.assessment_commands import (
    CompleteAssessmentCommand,
)
from app.application.assessment.handlers.complete_assessment_handler import (
    CompleteAssessmentHandler,
)
from app.application.common.exceptions.not_found_exception import (
    NotFoundException,
)
from app.domain.assessment.entities.assessment import Assessment
from app.domain.assessment.enums.assessment_status import AssessmentStatus
from app.domain.discovery.identifiers.discovery_id import DiscoveryId


def _assessment() -> Assessment:
    return Assessment(discovery_id=DiscoveryId())


@pytest.fixture
def unit_of_work():
    uow = AsyncMock()
    uow.__aenter__.return_value = uow
    uow.__aexit__.return_value = False
    return uow


@pytest.fixture
def handler(unit_of_work):
    return CompleteAssessmentHandler(unit_of_work=unit_of_work)


@pytest.mark.asyncio
async def test_completes_an_assessment_and_stamps_completed_at(handler, unit_of_work):
    assessment = _assessment()
    unit_of_work.assessment_repository.get_by_id.return_value = assessment

    result = await handler.handle(
        CompleteAssessmentCommand(assessment_id=str(assessment.id), summary="Ready for outreach.")
    )

    assert result.status == AssessmentStatus.COMPLETED
    assert result.summary == "Ready for outreach."
    assert assessment.completed_at is not None
    unit_of_work.assessment_repository.update.assert_awaited_once()


@pytest.mark.asyncio
async def test_completes_without_a_summary(handler, unit_of_work):
    assessment = _assessment()
    unit_of_work.assessment_repository.get_by_id.return_value = assessment

    result = await handler.handle(CompleteAssessmentCommand(assessment_id=str(assessment.id)))

    assert result.status == AssessmentStatus.COMPLETED
    assert result.summary is None


@pytest.mark.asyncio
async def test_raises_not_found_for_an_unknown_assessment(handler, unit_of_work):
    unit_of_work.assessment_repository.get_by_id.return_value = None

    with pytest.raises(NotFoundException):
        await handler.handle(CompleteAssessmentCommand(assessment_id=str(DiscoveryId())))

    unit_of_work.assessment_repository.update.assert_not_awaited()
