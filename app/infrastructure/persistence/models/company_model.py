"""
Company ORM model.
"""

from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.infrastructure.persistence.models.base_model import BaseModel


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

    industry: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    website: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    employee_count: Mapped[int | None] = mapped_column(
        nullable=True,
    )

    annual_revenue: Mapped[float | None] = mapped_column(
        nullable=True,
    )

    # -------------------------------------------------------------------------
    # Relationships
    # -------------------------------------------------------------------------

    leads: Mapped[list["LeadModel"]] = relationship(
        "LeadModel",
        back_populates="company",
    )