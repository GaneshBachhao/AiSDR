from typing import Generic

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import TypeVar

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """
    Standard API response wrapper.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    success: bool = True
    message: str | None = None
    data: T | None = None
    errors: list[str] = Field(default_factory=list)