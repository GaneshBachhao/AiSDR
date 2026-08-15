"""
Response DTO definitions.

Response DTOs represent completed application state and are
immutable after creation.
"""

from pydantic import ConfigDict

from app.application.common.dto.base_dto import BaseDTO


class ResponseDTO(BaseDTO):
    """
    Base class for immutable response DTOs.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_assignment=True,
        frozen=True,
    )