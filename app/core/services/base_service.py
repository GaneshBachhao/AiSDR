"""
Base Service

Provides common service functionality.
"""

from typing import Generic
from typing import TypeVar

from sqlalchemy.orm import Session

from app.schemas.common_schema import (
    PaginatedResponse,
)

ModelT = TypeVar(
    "ModelT",
)


class BaseService(
    Generic[ModelT],
):
    """
    Base class for business services.
    """

    def __init__(
        self,
        repository,
    ):
        self.repository = repository

    # =====================================================
    # Read
    # =====================================================

    def get_all(
        self,
        db: Session,
    ) -> list[ModelT]:

        return self.repository.get_all(
            db,
        )

    def get_by_id(
        self,
        db: Session,
        entity_id: int,
    ) -> ModelT | None:

        return self.repository.get_by_id(
            db,
            entity_id,
        )

    # =====================================================
    # Delete
    # =====================================================

    def delete(
        self,
        db: Session,
        entity,
    ) -> None:

        self.repository.delete(
            db,
            entity,
        )

    # =====================================================
    # Pagination
    # =====================================================

    def paginate(
        self,
        db: Session,
        page: int,
        size: int,
    ) -> PaginatedResponse:

        items = self.repository.paginate(
            db,
            page,
            size,
        )

        total_records = (
            self.repository.count(
                db,
            )
        )

        return PaginatedResponse.create(
            items=items,
            page=page,
            size=size,
            total_records=total_records,
        )