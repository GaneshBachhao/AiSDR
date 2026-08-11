"""
Request DTO definitions.

Request DTOs represent incoming application data and remain
mutable during application processing.
"""

from app.application.common.dto.base_dto import BaseDTO


class RequestDTO(BaseDTO):
    """
    Base class for mutable request DTOs.
    """

    pass