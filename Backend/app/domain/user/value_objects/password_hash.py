"""
PasswordHash value object.

Wraps an already-hashed password string. Hashing/verifying a plaintext
password against this value is an infrastructure concern (needs bcrypt,
a third-party runtime dependency the domain layer must not import) --
this value object only carries the hash and validates its shape.
"""

from __future__ import annotations

import re

_BCRYPT_PATTERN = re.compile(r"^\$2[aby]\$\d{2}\$.{53}$")


class PasswordHash:
    """
    Immutable value object representing an already-hashed password.

    Business rules:
    - The hash is mandatory and cannot be empty.
    - The hash must look like a real bcrypt hash, not a raw/plaintext
      string accidentally passed in.
    """

    def __init__(
        self,
        value: str,
    ) -> None:

        self._validate(value)

        self._value = value

    @property
    def value(self) -> str:
        return self._value

    def _validate(
        self,
        value: str,
    ) -> None:

        if not value:
            raise ValueError("Password hash cannot be empty.")

        if not _BCRYPT_PATTERN.match(value):
            raise ValueError("Password hash is not a valid bcrypt hash.")

    def __str__(self) -> str:
        return "PasswordHash(***)"

    def __repr__(self) -> str:
        return "PasswordHash(***)"

    def __eq__(
        self,
        other: object,
    ) -> bool:

        if not isinstance(other, PasswordHash):
            return False

        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)
