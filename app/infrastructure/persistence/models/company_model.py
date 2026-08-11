"""
Company ORM model.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.infrastructure.persistence.models.base_model import (
    BaseModel,
)

if TYPE_CHECKING:
    from app.infrastructure.persistence.models.lead_model import (
        LeadModel,
    )


class CompanyModel(BaseModel):
    """
    Represents a company within the persistence layer.
    """

    __tablename__ = "companies"

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        unique=True,
        index=True,
    )

    website: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    industry: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    company_size: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    country: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    state: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    city: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    employee_count: Mapped[int | None] = mapped_column(
        nullable=True,
    )

    annual_revenue: Mapped[float | None] = mapped_column(
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    # -------------------------------------------------------------------------
    # Relationships
    # -------------------------------------------------------------------------

    leads: Mapped[list["LeadModel"]] = relationship(
        "LeadModel",
        back_populates="company",
        cascade="all, delete-orphan",
    )