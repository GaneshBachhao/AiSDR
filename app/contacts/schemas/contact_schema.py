"""
Contact Schemas

Pydantic schemas used by the Contact domain.
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr
from pydantic import Field

from app.contacts.enums.contact_source import (
    ContactSource,
)

from app.contacts.enums.contact_status import (
    ContactStatus,
)


# ==========================================================
# Base
# ==========================================================


class ContactBase(BaseModel):
    """
    Shared contact fields.
    """

    first_name: str | None = Field(
        default=None,
        max_length=100,
    )

    last_name: str | None = Field(
        default=None,
        max_length=100,
    )

    full_name: str = Field(
        ...,
        max_length=255,
    )

    job_title: str | None = Field(
        default=None,
        max_length=255,
    )

    department: str | None = Field(
        default=None,
        max_length=100,
    )

    email: EmailStr

    phone: str | None = Field(
        default=None,
        max_length=50,
    )

    linkedin_url: str | None = None

    is_primary: bool = False

    status: ContactStatus = (
        ContactStatus.ACTIVE
    )

    source: ContactSource = (
        ContactSource.MANUAL
    )

    confidence_score: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )

    metadata_json: dict[str, Any] = Field(
        default_factory=dict,
    )


# ==========================================================
# Create
# ==========================================================


class ContactCreate(ContactBase):
    """
    Schema used when creating a contact.
    """

    lead_id: int


# ==========================================================
# Update
# ==========================================================


class ContactUpdate(BaseModel):
    """
    Schema used when updating a contact.
    """

    first_name: str | None = None

    last_name: str | None = None

    full_name: str | None = None

    job_title: str | None = None

    department: str | None = None

    email: EmailStr | None = None

    phone: str | None = None

    linkedin_url: str | None = None

    is_primary: bool | None = None

    status: ContactStatus | None = None

    source: ContactSource | None = None

    confidence_score: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
    )


# ==========================================================
# Response
# ==========================================================


class ContactResponse(ContactBase):
    """
    Contact returned from database.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int

    lead_id: int

    created_at: datetime

    updated_at: datetime

    last_verified_at: datetime | None = None