from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)

from sqlalchemy.sql import func

from app.database.database import Base


class Outreach(Base):
    """
    Stores AI-generated outreach communications
    for a lead.
    """

    __tablename__ = "outreach"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    lead_id = Column(
        Integer,
        ForeignKey("leads.id"),
        nullable=False,
        index=True,
    )

    lead_research_id = Column(
        Integer,
        ForeignKey("lead_research.id"),
        nullable=False,
        index=True,
    )

    channel = Column(
        String(50),
        nullable=False,
    )

    subject = Column(
        String(500),
        nullable=True,
    )

    message = Column(
        Text,
        nullable=False,
    )

    call_to_action = Column(
        Text,
        nullable=True,
    )

    status = Column(
        String(50),
        nullable=False,
        default="DRAFT",
    )

    version = Column(
        Integer,
        nullable=False,
        default=1,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )