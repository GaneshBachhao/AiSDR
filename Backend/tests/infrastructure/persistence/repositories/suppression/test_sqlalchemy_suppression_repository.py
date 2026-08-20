from __future__ import annotations

import pytest

from app.domain.contact.value_objects.email import Email
from app.domain.suppression.entities.suppression_entry import SuppressionEntry
from app.domain.suppression.enums.suppression_reason import SuppressionReason
from app.domain.suppression.identifiers.suppression_entry_id import SuppressionEntryId
from app.infrastructure.persistence.repositories.suppression.sqlalchemy_suppression_repository import (
    SqlAlchemySuppressionRepository,
)


@pytest.mark.asyncio
async def test_add_then_find_by_email_survives_reload(async_session):
    entry = SuppressionEntry(
        email=Email("Bounced@Example.com"),
        reason=SuppressionReason.BOUNCE,
        notes="Hard bounce.",
    )
    repo = SqlAlchemySuppressionRepository(async_session)
    await repo.add(entry)
    await async_session.commit()

    reload_repo = SqlAlchemySuppressionRepository(async_session)
    found = await reload_repo.find_by_email("bounced@example.com")

    assert found is not None
    assert found.email.value == "bounced@example.com"
    assert found.reason is SuppressionReason.BOUNCE
    assert found.notes == "Hard bounce."


@pytest.mark.asyncio
async def test_find_by_email_returns_none_when_not_suppressed(async_session):
    repo = SqlAlchemySuppressionRepository(async_session)

    found = await repo.find_by_email("nobody@example.com")

    assert found is None


@pytest.mark.asyncio
async def test_list_returns_added_entries(async_session):
    repo = SqlAlchemySuppressionRepository(async_session)
    await repo.add(SuppressionEntry(email=Email("a@example.com")))
    await repo.add(SuppressionEntry(email=Email("b@example.com")))
    await async_session.commit()

    entries = await repo.list()

    assert {entry.email.value for entry in entries} == {"a@example.com", "b@example.com"}


@pytest.mark.asyncio
async def test_delete_lifts_a_suppression(async_session):
    entry = SuppressionEntry(email=Email("lift-me@example.com"))
    repo = SqlAlchemySuppressionRepository(async_session)
    await repo.add(entry)
    await async_session.commit()

    await repo.delete(SuppressionEntryId(entry.id.value))
    await async_session.commit()

    reload_repo = SqlAlchemySuppressionRepository(async_session)
    found = await reload_repo.find_by_email("lift-me@example.com")
    assert found is None
