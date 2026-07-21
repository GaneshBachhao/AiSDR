from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
)

from sqlalchemy.sql import func

from app.database.database import Base


class Recommendation(Base):
    """
    Stores one AI solution recommendation generated
    for a Lead Research.
    """

    __tablename__ = "recommendations"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    lead_research_id = Column(
        Integer,
        ForeignKey("lead_research.id"),
        nullable=False,
        index=True
    )

    service_id = Column(
        String(100),
        nullable=False
    )

    service_name = Column(
        String(255),
        nullable=False
    )

    category = Column(
        String(100),
        nullable=True
    )

    priority = Column(
        String(20),
        nullable=True
    )

    difficulty = Column(
        String(20),
        nullable=True
    )

    roi = Column(
        String(1000),
        nullable=True
    )

    implementation_order = Column(
        Integer,
        nullable=False,
        default=1
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )