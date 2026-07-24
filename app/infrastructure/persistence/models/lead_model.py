"""
Lead SQLAlchemy model.

Mirror of the Lead aggregate.
"""

from __future__ import annotations

from sqlalchemy import Boolean
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.domain.lead.enums.lead_source import LeadSource
from app.domain.lead.enums.lead_status import LeadStatus
from app.infrastructure.persistence.database.base import Base
from app.infrastructure.persistence.database.base import EntityMixin


class LeadModel(Base, EntityMixin):
    """
    Persistence model for Lead aggregate.
    """

    __tablename__ = "leads"

    company_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    contact_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(320),
        nullable=False,
        unique=True,
        index=True,
    )

    phone: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    website: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    source: Mapped[LeadSource] = mapped_column(
        SqlEnum(
            LeadSource,
            name="lead_source",
        ),
        nullable=False,
        default=LeadSource.OTHER,
    )

    status: Mapped[LeadStatus] = mapped_column(
        SqlEnum(
            LeadStatus,
            name="lead_status",
        ),
        nullable=False,
        default=LeadStatus.NEW,
    )

    #
    # LeadScore value object
    #
    score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    notes: Mapped[str | None] = mapped_column(
        String(4000),
        nullable=True,
    )

    is_qualified: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )