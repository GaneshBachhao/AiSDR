"""
Email Model

Represents inbound and outbound email
communications associated with a Lead.
"""

from datetime import datetime, UTC

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    JSON,
    Enum,
    Index,
)

from sqlalchemy.orm import relationship

from app.database.database import Base

from app.emails.enums.email_status import (
    EmailStatus,
)

from app.emails.enums.email_direction import (
    EmailDirection,
)


class Email(Base):
    """
    Email communication record.
    """

    __tablename__ = "emails"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    # ==========================================================
    # Relationships
    # ==========================================================

    lead_id = Column(
        Integer,
        ForeignKey("leads.id"),
        nullable=False,
        index=True,
    )

    contact_id = Column(
        Integer,
        ForeignKey("contacts.id"),
        nullable=True,
        index=True,
    )

    conversation_id = Column(
        Integer,
        ForeignKey("conversations.id"),
        nullable=True,
        index=True,
    )

    lead = relationship(
        "Lead",
        back_populates="emails",
    )

    contact = relationship(
        "Contact",
        back_populates="emails",
    )

    conversation = relationship(
        "Conversation",
        back_populates="emails",
    )

    # ==========================================================
    # Email Content
    # ==========================================================

    subject = Column(
        String(500),
        nullable=False,
    )

    body = Column(
        Text,
        nullable=False,
    )

    # ==========================================================
    # Provider Information
    # ==========================================================

    provider = Column(
        String(50),
        nullable=False,
        default="gmail",
    )

    provider_message_id = Column(
        String(255),
        nullable=True,
        unique=True,
    )

    thread_id = Column(
        String(255),
        nullable=True,
        index=True,
    )

    external_reference = Column(
        String(255),
        nullable=True,
    )

    # ==========================================================
    # Status
    # ==========================================================

    status = Column(
        Enum(EmailStatus),
        nullable=False,
        default=EmailStatus.DRAFT,
        index=True,
    )

    direction = Column(
        Enum(EmailDirection),
        nullable=False,
        default=EmailDirection.OUTBOUND,
    )

    error_message = Column(
        Text,
        nullable=True,
    )

    # ==========================================================
    # Tracking
    # ==========================================================

    scheduled_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    sent_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    delivered_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    opened_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    clicked_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    replied_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    # ==========================================================
    # Metadata
    # ==========================================================

    metadata_json = Column(
        JSON,
        nullable=False,
        default=dict,
    )

    # ==========================================================
    # Audit
    # ==========================================================

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


Index(
    "idx_email_status",
    Email.status,
)

Index(
    "idx_email_thread",
    Email.thread_id,
)

Index(
    "idx_email_provider_message",
    Email.provider_message_id,
)