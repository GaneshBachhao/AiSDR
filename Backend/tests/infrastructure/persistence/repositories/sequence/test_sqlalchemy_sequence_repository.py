from __future__ import annotations

import pytest

from app.domain.lead.identifiers.lead_id import LeadId
from app.domain.sequence.entities.sequence import Sequence
from app.domain.sequence.enums.sequence_status import SequenceStatus
from app.domain.sequence.enums.touch_channel import TouchChannel
from app.domain.sequence.identifiers.sequence_id import SequenceId
from app.domain.sequence.value_objects.touch import Touch
from app.infrastructure.persistence.repositories.sequence.sqlalchemy_sequence_repository import (
    SqlAlchemySequenceRepository,
)


def _touches() -> list[Touch]:
    return [
        Touch(channel=TouchChannel.EMAIL, wait_days=0),
        Touch(channel=TouchChannel.LINKEDIN, wait_days=3),
        Touch(channel=TouchChannel.EMAIL, wait_days=4),
    ]


@pytest.mark.asyncio
async def test_add_then_get_by_id_preserves_touch_order_and_fields(async_session):
    lead_id = LeadId()
    sequence = Sequence(lead_id=lead_id, touches=_touches())
    repo = SqlAlchemySequenceRepository(async_session)
    await repo.add(sequence)
    await async_session.commit()

    reload_repo = SqlAlchemySequenceRepository(async_session)
    reloaded = await reload_repo.get_by_id(SequenceId(sequence.id.value))

    assert reloaded is not None
    assert reloaded.lead_id == lead_id
    assert [(t.channel, t.wait_days) for t in reloaded.touches] == [
        (TouchChannel.EMAIL, 0),
        (TouchChannel.LINKEDIN, 3),
        (TouchChannel.EMAIL, 4),
    ]
    assert reloaded.status is SequenceStatus.DRAFT


@pytest.mark.asyncio
async def test_update_changes_scalar_fields_and_leaves_touches_untouched(async_session):
    sequence = Sequence(lead_id=LeadId(), touches=_touches())
    repo = SqlAlchemySequenceRepository(async_session)
    await repo.add(sequence)
    await async_session.commit()

    loaded = await repo.get_by_id(sequence.id)
    loaded.start()
    loaded.advance()
    await repo.update(loaded)
    await async_session.commit()

    reload_repo = SqlAlchemySequenceRepository(async_session)
    reloaded = await reload_repo.get_by_id(SequenceId(sequence.id.value))

    assert reloaded.status is SequenceStatus.ACTIVE
    assert reloaded.current_touch_index == 1
    assert reloaded.started_at is not None
    assert len(reloaded.touches) == 3  # untouched by update()


@pytest.mark.asyncio
async def test_update_persists_touch_content_without_disturbing_other_touches(async_session):
    sequence = Sequence(lead_id=LeadId(), touches=_touches())
    repo = SqlAlchemySequenceRepository(async_session)
    await repo.add(sequence)
    await async_session.commit()

    loaded = await repo.get_by_id(sequence.id)
    loaded.set_touch_content(1, "Second touch: proof point about growth signals.")
    await repo.update(loaded)
    await async_session.commit()

    reload_repo = SqlAlchemySequenceRepository(async_session)
    reloaded = await reload_repo.get_by_id(SequenceId(sequence.id.value))

    assert reloaded.touches[0].content is None
    assert reloaded.touches[1].content == "Second touch: proof point about growth signals."
    assert reloaded.touches[2].content is None
    # Position/channel/wait_days untouched by the content update.
    assert [(t.channel, t.wait_days) for t in reloaded.touches] == [
        (TouchChannel.EMAIL, 0),
        (TouchChannel.LINKEDIN, 3),
        (TouchChannel.EMAIL, 4),
    ]


@pytest.mark.asyncio
async def test_list_by_lead_returns_only_that_leads_sequences(async_session):
    lead_id = LeadId()
    other_lead_id = LeadId()
    repo = SqlAlchemySequenceRepository(async_session)
    await repo.add(Sequence(lead_id=lead_id, touches=_touches()))
    await repo.add(Sequence(lead_id=other_lead_id, touches=_touches()))
    await async_session.commit()

    found = await repo.list_by_lead(lead_id)

    assert len(found) == 1
    assert found[0].lead_id == lead_id


@pytest.mark.asyncio
async def test_delete_removes_the_sequence_and_its_touches(async_session):
    sequence = Sequence(lead_id=LeadId(), touches=_touches())
    repo = SqlAlchemySequenceRepository(async_session)
    await repo.add(sequence)
    await async_session.commit()

    await repo.delete(SequenceId(sequence.id.value))
    await async_session.commit()

    reload_repo = SqlAlchemySequenceRepository(async_session)
    reloaded = await reload_repo.get_by_id(SequenceId(sequence.id.value))
    assert reloaded is None
