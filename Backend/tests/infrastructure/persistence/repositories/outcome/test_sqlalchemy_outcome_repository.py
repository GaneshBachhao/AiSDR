from __future__ import annotations

import pytest

from app.domain.lead.identifiers.lead_id import LeadId
from app.domain.outcome.entities.outcome_event import OutcomeEvent
from app.domain.outcome.enums.outcome_type import OutcomeType
from app.domain.outcome.identifiers.outcome_event_id import OutcomeEventId
from app.infrastructure.persistence.repositories.outcome.sqlalchemy_outcome_repository import (
    SqlAlchemyOutcomeRepository,
)


@pytest.mark.asyncio
async def test_add_then_list_by_lead_survives_reload(async_session):
    lead_id = LeadId()
    event = OutcomeEvent(
        lead_id=lead_id, outcome_type=OutcomeType.MEETING_BOOKED, notes="Booked via referral."
    )
    repo = SqlAlchemyOutcomeRepository(async_session)
    await repo.add(event)
    await async_session.commit()

    reload_repo = SqlAlchemyOutcomeRepository(async_session)
    found = await reload_repo.list_by_lead(lead_id)

    assert len(found) == 1
    assert found[0].outcome_type is OutcomeType.MEETING_BOOKED
    assert found[0].notes == "Booked via referral."


@pytest.mark.asyncio
async def test_list_by_lead_returns_multiple_events_for_the_same_lead(async_session):
    lead_id = LeadId()
    repo = SqlAlchemyOutcomeRepository(async_session)
    await repo.add(OutcomeEvent(lead_id=lead_id, outcome_type=OutcomeType.NO_RESPONSE))
    await repo.add(OutcomeEvent(lead_id=lead_id, outcome_type=OutcomeType.MEETING_BOOKED))
    await async_session.commit()

    found = await repo.list_by_lead(lead_id)

    assert {event.outcome_type for event in found} == {OutcomeType.NO_RESPONSE, OutcomeType.MEETING_BOOKED}


@pytest.mark.asyncio
async def test_list_by_lead_returns_empty_for_a_lead_with_no_events(async_session):
    repo = SqlAlchemyOutcomeRepository(async_session)

    found = await repo.list_by_lead(LeadId())

    assert found == []


@pytest.mark.asyncio
async def test_list_returns_all_events(async_session):
    repo = SqlAlchemyOutcomeRepository(async_session)
    await repo.add(OutcomeEvent(lead_id=LeadId(), outcome_type=OutcomeType.WON))
    await repo.add(OutcomeEvent(lead_id=LeadId(), outcome_type=OutcomeType.LOST))
    await async_session.commit()

    events = await repo.list()

    assert len(events) == 2


@pytest.mark.asyncio
async def test_delete_removes_an_outcome_event(async_session):
    event = OutcomeEvent(lead_id=LeadId(), outcome_type=OutcomeType.LOST)
    repo = SqlAlchemyOutcomeRepository(async_session)
    await repo.add(event)
    await async_session.commit()

    await repo.delete(OutcomeEventId(event.id.value))
    await async_session.commit()

    reload_repo = SqlAlchemyOutcomeRepository(async_session)
    found = await reload_repo.list_by_lead(event.lead_id)
    assert found == []
