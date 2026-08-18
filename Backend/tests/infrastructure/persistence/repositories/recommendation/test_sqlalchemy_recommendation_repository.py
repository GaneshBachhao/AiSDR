"""
Integration-level regression test: a Recommendation's status/submitted_at/
approved_at must survive a real save/update/reload cycle.

Before this fix, RecommendationModel had no columns for these fields at
all -- RecommendationMapper.to_domain hardcoded every loaded
Recommendation back to RecommendationStatus.DRAFT regardless of what had
actually happened to it. Submit/Approve appeared to work within a single
request/response (the in-memory domain object really did transition),
but the change was silently lost the moment anything reloaded the
aggregate -- discovered live via a real POST /submit followed by a real
GET showing status still "Draft".
"""

from __future__ import annotations

import pytest

from app.domain.assessment.entities.assessment import Assessment
from app.domain.discovery.identifiers.discovery_id import DiscoveryId
from app.domain.recommendation.entities.recommendation import Recommendation
from app.domain.recommendation.entities.solution import Solution
from app.domain.recommendation.identifiers.recommendation_id import RecommendationId
from app.infrastructure.persistence.repositories.assessment.sqlalchemy_assessment_repository import (
    SqlAlchemyAssessmentRepository,
)
from app.infrastructure.persistence.repositories.recommendation.sqlalchemy_recommendation_repository import (
    SqlAlchemyRecommendationRepository,
)


async def _persisted_assessment(async_session) -> Assessment:
    assessment = Assessment(
        discovery_id=DiscoveryId(),
        summary="Manual monthly reporting across disconnected spreadsheets.",
    )
    repo = SqlAlchemyAssessmentRepository(async_session)
    await repo.add(assessment)
    await async_session.commit()
    return assessment


@pytest.mark.asyncio
async def test_submit_then_approve_status_transitions_survive_reload(async_session):
    assessment = await _persisted_assessment(async_session)
    recommendation = Recommendation(assessment_id=assessment.id)
    recommendation.add_solution(
        Solution(
            title="Business Process Automation",
            description="Automate monthly reporting.",
            solution_type="Automation",
            priority="High",
            is_existing_offering=True,
        )
    )

    repo = SqlAlchemyRecommendationRepository(async_session)
    await repo.add(recommendation)
    await async_session.commit()

    # Submit, against a repository instance constructed fresh (simulates a
    # separate request), and reload again to prove it wasn't just an
    # in-memory transition.
    submit_repo = SqlAlchemyRecommendationRepository(async_session)
    loaded = await submit_repo.get_by_id(recommendation.id)
    loaded.submit()
    await submit_repo.update(loaded)
    await async_session.commit()

    reload_repo = SqlAlchemyRecommendationRepository(async_session)
    reloaded = await reload_repo.get_by_id(RecommendationId(recommendation.id.value))
    assert reloaded.status.value == "Under Review"
    assert reloaded.submitted_at is not None

    # Approve, same real-reload discipline.
    reloaded.approve()
    await reload_repo.update(reloaded)
    await async_session.commit()

    final_repo = SqlAlchemyRecommendationRepository(async_session)
    final = await final_repo.get_by_id(RecommendationId(recommendation.id.value))
    assert final.status.value == "Approved"
    assert final.approved_at is not None
    # update_model() must not disturb fields it doesn't own.
    assert len(final.solutions) == 1
    assert final.solutions[0].title == "Business Process Automation"
