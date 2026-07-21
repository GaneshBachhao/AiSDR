"""
Base Repository

Provides common CRUD operations for all repositories.
"""

from typing import Generic
from typing import TypeVar
from typing import Type

from sqlalchemy.orm import Session

ModelT = TypeVar("ModelT")


class BaseRepository(
    Generic[ModelT],
):
    """
    Base repository for SQLAlchemy models.
    """

    def __init__(
        self,
        model: Type[ModelT],
    ):
        self.model = model

    # =====================================================
    # Create
    # =====================================================

    def create(
        self,
        db: Session,
        entity: ModelT,
    ) -> ModelT:

        db.add(entity)

        db.commit()

        db.refresh(entity)

        return entity

    # =====================================================
    # Read
    # =====================================================

    def get_by_id(
        self,
        db: Session,
        entity_id: int,
    ) -> ModelT | None:

        return (
            db.query(self.model)
            .filter(
                self.model.id == entity_id
            )
            .first()
        )

    def get_all(
        self,
        db: Session,
    ) -> list[ModelT]:

        return (
            db.query(self.model)
            .all()
        )

    # =====================================================
    # Update
    # =====================================================

    def update(
        self,
        db: Session,
        entity: ModelT,
    ) -> ModelT:

        db.commit()

        db.refresh(entity)

        return entity

    # =====================================================
    # Delete
    # =====================================================

    def delete(
        self,
        db: Session,
        entity: ModelT,
    ) -> None:

        db.delete(entity)

        db.commit()

    # =====================================================
    # Count
    # =====================================================

    def count(
        self,
        db: Session,
    ) -> int:

        return (
            db.query(self.model)
            .count()
        )

    # =====================================================
    # Pagination
    # =====================================================

    def paginate(
        self,
        db: Session,
        page: int,
        size: int,
    ) -> list[ModelT]:

        offset = (
            page - 1
        ) * size

        return (
            db.query(self.model)
            .offset(offset)
            .limit(size)
            .all()
        )