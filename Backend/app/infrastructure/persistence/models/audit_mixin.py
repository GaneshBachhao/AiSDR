"""
Audit persistence mixin.

Provides audit information for persistent entities.
"""

from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class AuditMixin:
    """
    Adds audit information to a persistent entity.
    """

    created_by: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    updated_by: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
