from __future__ import annotations

import pytest

from app.domain.user.value_objects.password_hash import PasswordHash

_VALID_HASH = "$2b$12$" + ("N" * 53)


def test_password_hash_accepts_a_bcrypt_shaped_string() -> None:
    password_hash = PasswordHash(_VALID_HASH)

    assert password_hash.value == _VALID_HASH


def test_password_hash_rejects_empty_string() -> None:
    with pytest.raises(ValueError):
        PasswordHash("")


@pytest.mark.parametrize(
    "invalid",
    [
        "hunter2",
        "not-a-bcrypt-hash",
        "$2b$12$too-short",
    ],
)
def test_password_hash_rejects_non_bcrypt_shaped_strings(invalid: str) -> None:
    with pytest.raises(ValueError):
        PasswordHash(invalid)


def test_password_hash_equality_by_value() -> None:
    assert PasswordHash(_VALID_HASH) == PasswordHash(_VALID_HASH)
    assert hash(PasswordHash(_VALID_HASH)) == hash(PasswordHash(_VALID_HASH))


def test_password_hash_repr_and_str_do_not_leak_the_raw_value() -> None:
    password_hash = PasswordHash(_VALID_HASH)

    assert _VALID_HASH not in repr(password_hash)
    assert _VALID_HASH not in str(password_hash)
