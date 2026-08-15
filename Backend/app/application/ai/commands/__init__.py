"""
Execute AI Request Command

Represents a request to execute an AI completion.
"""

from pydantic import BaseModel, ConfigDict, Field


class ExecuteAIRequestCommand(BaseModel):
    """
    Command used by ExecuteAIRequestHandler.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        str_strip_whitespace=True,
    )

    provider: str = Field(
        ...,
        min_length=2,
        max_length=50,
    )

    model: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    prompt: str = Field(
        ...,
        min_length=1,
    )

    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
    )

    max_tokens: int = Field(
        default=1024,
        ge=1,
        le=32768,
    )