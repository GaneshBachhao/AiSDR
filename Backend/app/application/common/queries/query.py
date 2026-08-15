# app/application/common/queries/query.py

"""
Base application query.

Queries are immutable request models used for read operations.
"""

from pydantic import ConfigDict

from app.application.common.dto.request_dto import (
    RequestDTO,
)


class Query(RequestDTO):
    """
    Base query model.

    Queries are immutable to guarantee predictable execution.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_assignment=True,
        frozen=True,
    )