"""
SuppressionEntry ORM model.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.persistence.models.base_model import BaseModel


class SuppressionEntryModel(BaseModel):
    """
    Represents a do-not-contact email address within the persistence layer.
    """

    __tablename__ = "suppression_entries"

    email: Mapped[str] = mapped_column(
        String(320),
        nullable=False,
        unique=True,
        index=True,
    )

    reason: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="Manual",
    )

    notes: Mapped[str | None] = mapped_column(
        String(2000),
        nullable=True,
    )

    suppressed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
