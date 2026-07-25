"""
Lead ORM model.
"""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.infrastructure.persistence.models.base_model import BaseModel
from app.infrastructure.persistence.models.company_model import CompanyModel


class LeadModel(BaseModel):
    """
    Represents a sales lead.
    """

    __tablename__ = "leads"

    company_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        ForeignKey(
            "companies.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
        index=True,
    )

    contact_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(320),
        nullable=False,
        index=True,
    )

    phone: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    job_title: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    # -------------------------------------------------------------------------
    # Relationships
    # -------------------------------------------------------------------------

    company: Mapped[CompanyModel] = relationship(
        back_populates="leads",
        lazy="joined",
    )

    discoveries: Mapped[list["DiscoveryModel"]] = relationship(
        "DiscoveryModel",
        back_populates="lead",
        cascade="all, delete-orphan",
    )