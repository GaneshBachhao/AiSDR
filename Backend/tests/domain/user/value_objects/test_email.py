from __future__ import annotations

import pytest

from app.domain.user.value_objects.email import Email


def test_email_normalizes_case_and_whitespace() -> None:
    email = Email("  Jane.Doe@Example.COM  ")

    assert email.value == "jane.doe@example.com"


def test_email_equality_and_hash_by_value() -> None:
    assert Email("jane@example.com") == Email("Jane@Example.com")
    assert hash(Email("jane@example.com")) == hash(Email("Jane@Example.com"))


def test_email_rejects_empty_string() -> None:
    with pytest.raises(ValueError):
        Email("   ")


@pytest.mark.parametrize(
    "invalid",
    [
        "not-an-email",
        "missing-domain@",
        "@missing-local.com",
        "no-at-sign.example.com",
    ],
)
def test_email_rejects_invalid_format(invalid: str) -> None:
    with pytest.raises(ValueError):
        Email(invalid)
