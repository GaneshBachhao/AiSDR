"""
Lead persistence model.

A Lead belongs to a Company/Account and references a Contact.
Contact details are owned by the Contact aggregate.
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.persistence.models.base_model import BaseModel
from app.infrastructure.persistence.sqlalchemy.lead_score_type import LeadScoreType

if TYPE_CHECKING:
    from app.infrastructure.persistence.models.company_model import CompanyModel
    from app.infrastructure.persistence.models.discovery_model import DiscoveryModel


class LeadModel(BaseModel):
    """Database representation of Lead."""

    __tablename__ = "leads"

    company_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        ForeignKey("companies.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    contact_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        ForeignKey("contacts.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    source: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="Other",
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="New",
    )

    score: Mapped[int] = mapped_column(
        LeadScoreType(),
        nullable=False,
        default=0,
    )

    notes: Mapped[str | None] = mapped_column(
        String(5000),
        nullable=True,
    )

    is_qualified: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    review_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="Not Submitted",
    )

    review_submitted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    review_decided_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    review_notes: Mapped[str | None] = mapped_column(
        String(2000),
        nullable=True,
    )

    # Buying-signal categories detected at creation time by AI research
    # (EPIC-12). NULL means "not captured" (e.g. a manually-created Lead
    # that never went through company_research) -- distinct from False,
    # which means the category was checked for and absent.
    signal_hiring: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    signal_growth: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    signal_technology: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    signal_ai: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    signal_process: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    signal_funding: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    company: Mapped[CompanyModel] = relationship(
        "CompanyModel",
        back_populates="leads",
        lazy="joined",
    )

    discoveries: Mapped[list[DiscoveryModel]] = relationship(
        "DiscoveryModel",
        back_populates="lead",
        passive_deletes=True,
    )
