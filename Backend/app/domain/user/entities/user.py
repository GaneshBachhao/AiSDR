from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.shared.base.aggregate_root import AggregateRoot
from app.domain.user.identifiers.user_id import UserId
from app.domain.user.value_objects.email import Email
from app.domain.user.value_objects.password_hash import PasswordHash


@dataclass(eq=False)
class User(AggregateRoot[UserId]):
    """
    Aggregate root representing an operator-provisioned login account.

    There is no self-service registration -- accounts are created by a
    human operator (see Backend/scripts/create_user.py), so this
    aggregate has no "register" factory beyond plain construction.
    """

    id: UserId = field(
        default_factory=UserId,
        kw_only=True,
    )

    email: Email
    password_hash: PasswordHash
    is_active: bool = True

    def activate(self) -> None:
        self.is_active = True
        self.touch()

    def deactivate(self) -> None:
        self.is_active = False
        self.touch()

    def change_password(self, password_hash: PasswordHash) -> None:
        self.password_hash = password_hash
        self.touch()
