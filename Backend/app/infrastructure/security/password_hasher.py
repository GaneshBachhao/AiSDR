"""
Password hashing, backed by bcrypt.

Kept separate from the domain layer's PasswordHash value object, which
only carries an already-hashed string -- bcrypt is a third-party runtime
dependency the domain layer must not import.
"""

from __future__ import annotations

import bcrypt


class PasswordHasher:
    """Hashes and verifies plaintext passwords using bcrypt."""

    def hash(self, plain: str) -> str:
        return bcrypt.hashpw(
            plain.encode("utf-8"),
            bcrypt.gensalt(),
        ).decode("utf-8")

    def verify(self, plain: str, hashed: str) -> bool:
        try:
            return bcrypt.checkpw(
                plain.encode("utf-8"),
                hashed.encode("utf-8"),
            )
        except (ValueError, TypeError):
            # A malformed/foreign hash string must fail closed, not raise --
            # this is called on the login path with data that ultimately
            # traces back to persisted storage, and a corrupt row should
            # behave the same as "wrong password," not crash the request.
            return False
