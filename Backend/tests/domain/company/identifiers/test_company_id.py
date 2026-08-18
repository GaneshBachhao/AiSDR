from __future__ import annotations

from uuid import UUID, uuid4

import pytest

from app.domain.company.identifiers.company_id import CompanyId


def test_generates_a_real_uuid_when_no_value_given() -> None:
    company_id = CompanyId()

    assert isinstance(company_id.value, UUID)


def test_accepts_an_explicit_uuid() -> None:
    raw = uuid4()

    company_id = CompanyId(raw)

    assert company_id.value == raw


def test_accepts_a_string_uuid() -> None:
    raw = uuid4()

    company_id = CompanyId(str(raw))

    assert company_id.value == raw


def test_rejects_a_malformed_string() -> None:
    with pytest.raises(ValueError):
        CompanyId("not-a-uuid")


def test_equality_and_hash_by_value() -> None:
    raw = uuid4()

    assert CompanyId(raw) == CompanyId(raw)
    assert hash(CompanyId(raw)) == hash(CompanyId(raw))


def test_two_generated_ids_are_distinct() -> None:
    assert CompanyId() != CompanyId()
