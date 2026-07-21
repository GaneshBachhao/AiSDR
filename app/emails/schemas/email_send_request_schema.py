"""
Email Send Request Schema

Application layer request passed
to an email provider.
"""

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field


class EmailSendRequest(BaseModel):
    """
    Request passed to an email provider.
    """

    to_email: EmailStr

    subject: str = Field(
        ...,
        max_length=500,
    )

    html_body: str

    text_body: str | None = None