"""
User repository contract.

Defines the application-facing persistence contract for User.
"""
from __future__ import annotations

from abc import abstractmethod

from app.application.common.interfaces.repository import Repository
from app.domain.user.entities.user import User
from app.domain.user.identifiers.user_id import UserId


class UserRepository(Repository[User, UserId]):
    """Repository contract for User aggregates."""

    @abstractmethod
    async def find_by_email(self, email: str) -> User | None:
        raise NotImplementedError
