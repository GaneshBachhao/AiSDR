"""
Contact API request schemas.
"""

from __future__ import annotations

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr


class CreateContactRequest(BaseModel):
    """
    Create Contact request.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    company_id: str

    first_name: str

    last_name: str

    email: EmailStr

    phone: str | None = None

    job_title: str | None = None

    linkedin_url: str | None = None


class UpdateContactRequest(BaseModel):
    """
    Update Contact request.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    first_name: str | None = None

    last_name: str | None = None

    email: EmailStr | None = None

    phone: str | None = None

    job_title: str | None = None

    linkedin_url: str | None = None