from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CreateLeadRequest(BaseModel):
    """
    Create lead request schema.
    """

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    company_name: str = Field(
        ...,
        min_length=2,
        max_length=200,
    )

    contact_name: str = Field(
        ...,
        min_length=2,
        max_length=200,
    )

    email: EmailStr

    phone: str | None = Field(
        default=None,
        max_length=30,
    )

    website: str | None = None

    notes: str | None = None