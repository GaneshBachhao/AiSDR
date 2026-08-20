"""
Integration-level regression test: a Lead's review-gate state
(review_status/review_submitted_at/review_decided_at/review_notes) must
survive a real save/update/reload cycle.

Before this fix, SqlAlchemyLeadRepository had no update() override -- it
fell through to the generic base (session.merge(mapper.to_model(entity))),
which merges a freshly-constructed model that never sets the BaseModel
audit-mixin columns (created_by/updated_by/is_deleted/deleted_at),
silently clobbering them back to their Python defaults on every save.
LeadMapper.update_model() already existed for exactly this but was never
called by anything -- the same bug class already found and fixed for
Recommendation.
"""

from __future__ import annotations

import pytest

from app.domain.company.identifiers.company_id import CompanyId
from app.domain.contact.identifiers.contact_id import ContactId
from app.domain.lead.entities.lead import Lead
from app.domain.lead.identifiers.lead_id import LeadId
from app.infrastructure.persistence.repositories.lead.sqlalchemy_lead_repository import (
    SqlAlchemyLeadRepository,
)


@pytest.mark.asyncio
async def test_submit_then_approve_review_gate_survives_reload(async_session):
    lead = Lead(company_id=CompanyId(), contact_id=ContactId())

    repo = SqlAlchemyLeadRepository(async_session)
    await repo.add(lead)
    await async_session.commit()

    # Submit, against a repository instance constructed fresh (simulates a
    # separate request), and reload again to prove it wasn't just an
    # in-memory transition.
    submit_repo = SqlAlchemyLeadRepository(async_session)
    loaded = await submit_repo.get_by_id(lead.id)
    loaded.submit_for_review()
    await submit_repo.update(loaded)
    await async_session.commit()

    reload_repo = SqlAlchemyLeadRepository(async_session)
    reloaded = await reload_repo.get_by_id(LeadId(lead.id.value))
    assert reloaded.review_status.value == "Pending Review"
    assert reloaded.review_submitted_at is not None

    # Approve, same real-reload discipline.
    reloaded.approve(notes="Confirmed a real decision maker.")
    await reload_repo.update(reloaded)
    await async_session.commit()

    final_repo = SqlAlchemyLeadRepository(async_session)
    final = await final_repo.get_by_id(LeadId(lead.id.value))
    assert final.review_status.value == "Approved"
    assert final.review_decided_at is not None
    assert final.review_notes == "Confirmed a real decision maker."
    # update_model() must not disturb fields it doesn't own.
    assert final.company_id == lead.company_id
    assert final.contact_id == lead.contact_id


@pytest.mark.asyncio
async def test_reject_then_resubmit_survives_reload(async_session):
    lead = Lead(company_id=CompanyId(), contact_id=ContactId())
    repo = SqlAlchemyLeadRepository(async_session)
    await repo.add(lead)
    await async_session.commit()

    loaded = await repo.get_by_id(lead.id)
    loaded.submit_for_review()
    loaded.reject(notes="No verified email yet.")
    await repo.update(loaded)
    await async_session.commit()

    reload_repo = SqlAlchemyLeadRepository(async_session)
    reloaded = await reload_repo.get_by_id(LeadId(lead.id.value))
    assert reloaded.review_status.value == "Rejected"
    assert reloaded.review_notes == "No verified email yet."

    reloaded.submit_for_review()
    await reload_repo.update(reloaded)
    await async_session.commit()

    final_repo = SqlAlchemyLeadRepository(async_session)
    final = await final_repo.get_by_id(LeadId(lead.id.value))
    assert final.review_status.value == "Pending Review"


@pytest.mark.asyncio
async def test_evidence_signals_survive_reload(async_session):
    """
    Regression coverage for the new flatten/unflatten logic (EPIC-12):
    Lead.evidence_signals (a dict) round-trips through 6 flat boolean
    columns on LeadModel via LeadMapper -- the real risk area this sprint,
    same caution as the earlier update() bug.
    """
    lead = Lead(
        company_id=CompanyId(),
        contact_id=ContactId(),
        evidence_signals={
            "hiring": True,
            "growth": False,
            "technology": True,
            "ai": False,
            "process": False,
            "funding": True,
        },
    )

    repo = SqlAlchemyLeadRepository(async_session)
    await repo.add(lead)
    await async_session.commit()

    reload_repo = SqlAlchemyLeadRepository(async_session)
    reloaded = await reload_repo.get_by_id(LeadId(lead.id.value))

    assert reloaded.evidence_signals == {
        "hiring": True,
        "growth": False,
        "technology": True,
        "ai": False,
        "process": False,
        "funding": True,
    }


@pytest.mark.asyncio
async def test_evidence_signals_none_stays_none_not_a_dict_of_false(async_session):
    lead = Lead(company_id=CompanyId(), contact_id=ContactId())

    repo = SqlAlchemyLeadRepository(async_session)
    await repo.add(lead)
    await async_session.commit()

    reload_repo = SqlAlchemyLeadRepository(async_session)
    reloaded = await reload_repo.get_by_id(LeadId(lead.id.value))

    assert reloaded.evidence_signals is None
