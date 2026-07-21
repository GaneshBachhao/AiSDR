"""
Generated Email Schema

Represents AI-generated email content.
"""

from pydantic import BaseModel, Field


class GeneratedEmail(BaseModel):
    """
    AI generated email.
    """

    subject: str = Field(
        min_length=1,
        max_length=250,
    )

    body: str = Field(
        min_length=1,
    )