from uuid import UUID, uuid4

import pytest

from app.domain.company.identifiers.company_id import CompanyId


def test_identifier_generates_uuid() -> None:
    identifier = CompanyId()
    assert isinstance(identifier.value, UUID)


def test_identifier_parses_uuid_string() -> None:
    value = uuid4()
    identifier = CompanyId(str(value))
    assert identifier.value == value


def test_identifier_rejects_invalid_uuid() -> None:
    with pytest.raises(ValueError):
        CompanyId("company-123")


def test_identifier_rejects_empty_string() -> None:
    with pytest.raises(ValueError):
        CompanyId("   ")
