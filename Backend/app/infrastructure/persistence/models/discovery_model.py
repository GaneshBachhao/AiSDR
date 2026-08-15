"""
Discovery ORM model.
"""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.infrastructure.persistence.models.base_model import BaseModel
from app.infrastructure.persistence.models.lead_model import LeadModel


class DiscoveryModel(BaseModel):
    """
    Represents a discovery session for a lead.
    """

    __tablename__ = "discoveries"

    lead_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        ForeignKey(
            "leads.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    current_process: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    challenges: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    goals: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="Pending",
    )

    # -------------------------------------------------------------------------
    # Relationships
    # -------------------------------------------------------------------------

    lead: Mapped[LeadModel] = relationship(
        back_populates="discoveries",
        lazy="joined",
    )

    assessment: Mapped["AssessmentModel | None"] = relationship(
        "AssessmentModel",
        back_populates="discovery",
        uselist=False,
        cascade="all, delete-orphan",
    )