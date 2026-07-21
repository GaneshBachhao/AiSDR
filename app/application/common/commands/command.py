# app/application/common/commands/command.py

"""
Base application command.

Commands are immutable messages representing an intention
to execute a business operation.
"""

from pydantic import ConfigDict

from app.application.common.dto.request_dto import (
    RequestDTO,
)


class Command(RequestDTO):
    """
    Base command model.

    Commands are request DTOs with immutability enabled to ensure
    handlers receive a stable operation request.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_assignment=True,
        frozen=True,
    )