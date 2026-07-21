"""
Contact Model

Represents an individual contact
belonging to a Lead.
"""

from datetime import UTC, datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    JSON,
    String,
)

from sqlalchemy.orm import relationship

from app.database.database import Base

from app.contacts.enums.contact_source import ContactSource
from app.contacts.enums.contact_status import ContactStatus


class Contact(Base):
    """
    Lead contact.
    """

    __tablename__ = "contacts"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    # ======================================================
    # Relationships
    # ======================================================

    lead_id = Column(
        Integer,
        ForeignKey("leads.id"),
        nullable=False,
        index=True,
    )

    lead = relationship(
        "Lead",
        back_populates="contacts",
    )

    emails = relationship(
        "Email",
        back_populates="contact",
        cascade="all, delete-orphan",
    )

    conversations = relationship(
        "Conversation",
        back_populates="contact",
        cascade="all, delete-orphan",
    )

    # ======================================================
    # Personal
    # ======================================================

    first_name = Column(
        String(100),
        nullable=True,
    )

    last_name = Column(
        String(100),
        nullable=True,
    )

    full_name = Column(
        String(255),
        nullable=False,
    )

    # ======================================================
    # Business
    # ======================================================

    job_title = Column(
        String(255),
        nullable=True,
    )

    department = Column(
        String(100),
        nullable=True,
    )

    # ======================================================
    # Contact
    # ======================================================

    email = Column(
        String(255),
        nullable=False,
        index=True,
    )

    phone = Column(
        String(50),
        nullable=True,
    )

    linkedin_url = Column(
        String(500),
        nullable=True,
    )

    # ======================================================
    # Flags
    # ======================================================

    is_primary = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    status = Column(
        Enum(ContactStatus),
        default=ContactStatus.ACTIVE,
        nullable=False,
    )

    source = Column(
        Enum(ContactSource),
        default=ContactSource.MANUAL,
        nullable=False,
    )

    confidence_score = Column(
        Float,
        default=1.0,
        nullable=False,
    )

    last_verified_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    metadata_json = Column(
        JSON,
        nullable=False,
        default=dict,
    )

    # ======================================================
    # Audit
    # ======================================================

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )