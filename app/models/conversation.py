"""
Conversation Model

Represents an email conversation (thread)
between AgneticAI and a contact.
"""

from datetime import UTC
from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
)

from sqlalchemy.orm import relationship

from app.conversations.enums.conversation_status import (
    ConversationStatus,
)

from app.database.database import Base


class Conversation(Base):
    """
    Email conversation.
    """

    __tablename__ = "conversations"

    # ======================================================
    # Identity
    # ======================================================

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

    contact_id = Column(
        Integer,
        ForeignKey("contacts.id"),
        nullable=False,
        index=True,
    )

    lead = relationship(
        "Lead",
        back_populates="conversations",
    )

    contact = relationship(
        "Contact",
        back_populates="conversations",
    )

    # ======================================================
    # Provider
    # ======================================================

    provider = Column(
        String(50),
        nullable=False,
        default="gmail",
    )

    provider_thread_id = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    # ======================================================
    # Status
    # ======================================================

    status = Column(
        Enum(ConversationStatus),
        nullable=False,
        default=ConversationStatus.OPEN,
        index=True,
    )

    # ======================================================
    # Timeline
    # ======================================================

    started_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    last_message_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    closed_at = Column(
        DateTime(timezone=True),
        nullable=True,
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

    # ======================================================
    # Emails
    # ======================================================

    emails = relationship(
        "Email",
        back_populates="conversation",
        cascade="all, delete-orphan",
    )