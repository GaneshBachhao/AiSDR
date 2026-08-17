from __future__ import annotations

from app.infrastructure.security.password_hasher import PasswordHasher


def test_hash_produces_a_bcrypt_shaped_string_different_from_the_input() -> None:
    hasher = PasswordHasher()

    hashed = hasher.hash("correct horse battery staple")

    assert hashed != "correct horse battery staple"
    assert hashed.startswith("$2b$")


def test_verify_true_for_the_correct_plain_hash_pair() -> None:
    hasher = PasswordHasher()
    hashed = hasher.hash("hunter2")

    assert hasher.verify("hunter2", hashed) is True


def test_verify_false_for_the_wrong_password() -> None:
    hasher = PasswordHasher()
    hashed = hasher.hash("hunter2")

    assert hasher.verify("wrong-password", hashed) is False


def test_verify_false_not_raise_for_a_garbage_hash_string() -> None:
    hasher = PasswordHasher()

    assert hasher.verify("hunter2", "not-a-real-hash") is False
