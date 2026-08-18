from __future__ import annotations

from app.domain.company.events.company_updated import CompanyUpdated


def test_company_updated_carries_the_company_id() -> None:
    event = CompanyUpdated(company_id="c1")

    assert event.company_id == "c1"


def test_company_updated_gets_a_real_event_id_and_timestamp() -> None:
    event = CompanyUpdated(company_id="c1")

    assert event.event_id is not None
    assert event.occurred_at is not None
