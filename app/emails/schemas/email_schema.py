"""
Email Schemas

Pydantic schemas used by the Email domain.
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.emails.enums.email_direction import (
    EmailDirection,
)

from app.emails.enums.email_status import (
    EmailStatus,
)


# ==========================================================
# Base
# ==========================================================


class EmailBase(BaseModel):
    """
    Shared email fields.
    """

    subject: str = Field(
        ...,
        max_length=500,
    )

    body: str

    provider: str = Field(
        default="gmail",
    )

    direction: EmailDirection = (
        EmailDirection.OUTBOUND
    )

    scheduled_at: datetime | None = None

    metadata_json: dict[str, Any] = Field(
        default_factory=dict,
    )


# ==========================================================
# Create
# ==========================================================


class EmailCreate(EmailBase):
    """
    Schema used when creating an email.
    """

    lead_id: int

    contact_id: int | None = None


# ==========================================================
# Update
# ==========================================================


class EmailUpdate(BaseModel):
    """
    Schema used when updating an email.
    """

    subject: str | None = None

    body: str | None = None

    status: EmailStatus | None = None

    provider_message_id: str | None = None

    thread_id: str | None = None

    external_reference: str | None = None

    error_message: str | None = None

    scheduled_at: datetime | None = None

    sent_at: datetime | None = None

    delivered_at: datetime | None = None

    opened_at: datetime | None = None

    clicked_at: datetime | None = None

    replied_at: datetime |None = None

    metadata_json: dict[str, Any] | None = None


# ==========================================================
# Response
# ==========================================================


class EmailResponse(EmailBase):
    """
    Email returned from the database.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int

    lead_id: int

    contact_id: int | None = None

    status: EmailStatus

    provider_message_id: str | None = None

    thread_id: str | None = None

    external_reference: str | None = None

    error_message: str | None = None

    sent_at: datetime | None = None

    delivered_at: datetime | None = None

    opened_at: datetime | None = None

    clicked_at: datetime | None = None

    replied_at: datetime | None = None

    created_at: datetime

    updated_at: datetime