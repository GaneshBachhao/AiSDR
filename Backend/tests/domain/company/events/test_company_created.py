from __future__ import annotations

from app.domain.company.events.company_created import CompanyCreated


def test_company_created_carries_the_real_fields() -> None:
    event = CompanyCreated(company_id="c1", company_name="Acme")

    assert event.company_id == "c1"
    assert event.company_name == "Acme"


def test_company_created_gets_a_real_event_id_and_timestamp() -> None:
    # Regression guard: DomainEvent used to be a plain class with a
    # hand-written __init__ that a @dataclass subclass's generated
    # __init__ never called -- event_id/occurred_at raised AttributeError
    # on every concrete event in the codebase. Never surfaced because
    # nothing raises these events yet.
    event = CompanyCreated(company_id="c1", company_name="Acme")

    assert event.event_id is not None
    assert event.occurred_at is not None


def test_two_events_get_distinct_event_ids() -> None:
    first = CompanyCreated(company_id="c1", company_name="Acme")
    second = CompanyCreated(company_id="c1", company_name="Acme")

    assert first.event_id != second.event_id
