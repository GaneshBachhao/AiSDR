from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)

from sqlalchemy.orm import relationship

from app.database.database import Base


class LeadResearch(Base):
    __tablename__ = "lead_research"

    id = Column(Integer, primary_key=True, index=True)

    lead_id = Column(
        Integer,
        ForeignKey("leads.id"),
        nullable=False
    )

    company_name = Column(String, nullable=False)

    industry = Column(String)

    summary = Column(Text)

    business_model = Column(Text)

    pain_points = Column(Text)

    ai_opportunities = Column(Text)

    recommended_services = Column(Text)

    decision_makers = Column(Text)

    buying_signals = Column(Text)

    confidence_score = Column(Float)

    matched_sector = Column(
        String(100),
        nullable=True
    )

    sector_confidence = Column(
        Float,
        nullable=True
    )

    catalog_services = Column(
        Text,
        nullable=True
    )

    generic_ai_opportunities = Column(
        Text,
        nullable=True
    )

    catalog_version = Column(
        String(20),
        nullable=True
    )

    model_name = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    lead = relationship(
        "Lead",
        back_populates="research"
    )