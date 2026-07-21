"""
Standard API Response
"""

from typing import Generic
from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(
    BaseModel,
    Generic[T],
):
    """
    Standard response wrapper.
    """

    success: bool = True

    message: str = "Success"

    data: T | None = None