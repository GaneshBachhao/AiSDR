"""
SQLAlchemy implementation of UserRepository.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.contracts.repositories.user_repository import (
    UserRepository,
)
from app.domain.user.entities.user import User
from app.domain.user.identifiers.user_id import UserId
from app.infrastructure.persistence.mappers.user_mapper import UserMapper
from app.infrastructure.persistence.models.user_model import UserModel
from app.infrastructure.persistence.repositories.base.sqlalchemy_repository import (
    SqlAlchemyRepository,
)


class SqlAlchemyUserRepository(
    SqlAlchemyRepository[User, UserModel, UserId],
    UserRepository,
):
    """SQLAlchemy User repository."""

    model_type = UserModel

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, mapper=UserMapper())

    async def find_by_email(self, email: str) -> User | None:
        result = await self._session.execute(
            select(UserModel).where(UserModel.email == email.strip().lower())
        )
        model = result.scalar_one_or_none()
        return None if model is None else self.mapper.to_domain(model)

    async def update(self, entity: User) -> None:
        """
        Update the already-persisted ORM row in place.

        This avoids merging a newly-created ORM instance with missing
        server-managed timestamp/audit fields.
        """
        db_id = entity.id.value
        model = await self._session.get(UserModel, db_id)

        if model is None:
            return

        self.mapper.update_model(model, entity)
