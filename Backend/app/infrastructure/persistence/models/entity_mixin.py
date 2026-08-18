"""
Entity persistence mixin.

Provides the primary key shared by all persistent entities.
"""

from __future__ import annotations

from uuid import UUID, uuid4

from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column


class EntityMixin:
    """
    Adds the primary key to a persistent entity.
    """

    id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        nullable=False,
    )
