from __future__ import annotations

from app.domain.user.entities.user import User
from app.domain.user.value_objects.email import Email
from app.domain.user.value_objects.password_hash import PasswordHash

_VALID_HASH = "$2b$12$" + ("N" * 53)


def _make_user(**overrides) -> User:
    defaults = {
        "email": Email("jane@example.com"),
        "password_hash": PasswordHash(_VALID_HASH),
    }
    defaults.update(overrides)
    return User(**defaults)


def test_user_defaults_to_active() -> None:
    user = _make_user()

    assert user.is_active is True


def test_user_deactivate_and_activate_toggle_state_and_touch() -> None:
    user = _make_user()
    updated_before = user.updated_at

    user.deactivate()

    assert user.is_active is False
    assert user.updated_at >= updated_before

    user.activate()

    assert user.is_active is True


def test_user_change_password_replaces_hash_and_touches() -> None:
    user = _make_user()
    new_hash = PasswordHash("$2b$12$" + ("M" * 53))

    user.change_password(new_hash)

    assert user.password_hash == new_hash
