"""
User persistence mapper.

Domain <-> ORM conversion always unwraps strongly typed IDs to UUIDs
when constructing ORM models.
"""

from __future__ import annotations

from app.domain.user.entities.user import User
from app.domain.user.identifiers.user_id import UserId
from app.domain.user.value_objects.email import Email
from app.domain.user.value_objects.password_hash import PasswordHash
from app.infrastructure.persistence.models.user_model import UserModel


class UserMapper:
    """Maps User domain entities and ORM models."""

    @staticmethod
    def to_domain(model: UserModel) -> User:
        user = User(
            id=UserId(model.id),
            email=Email(model.email),
            password_hash=PasswordHash(model.password_hash),
            is_active=model.is_active,
        )
        user.created_at = model.created_at
        user.updated_at = model.updated_at
        return user

    @staticmethod
    def to_model(entity: User) -> UserModel:
        return UserModel(
            id=entity.id.value,
            email=entity.email.value,
            password_hash=entity.password_hash.value,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    @staticmethod
    def update_model(
        model: UserModel,
        entity: User,
    ) -> UserModel:
        model.email = entity.email.value
        model.password_hash = entity.password_hash.value
        model.is_active = entity.is_active
        return model
