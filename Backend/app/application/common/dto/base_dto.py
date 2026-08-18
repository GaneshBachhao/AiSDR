"""
Base DTO configuration.

All Application layer DTOs inherit from this class to ensure
consistent validation and serialization behavior.
"""

from pydantic import BaseModel, ConfigDict


class BaseDTO(BaseModel):
    """
    Base class for all Application DTOs.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )
