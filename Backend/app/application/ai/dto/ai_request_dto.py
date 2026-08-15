"""
AI Request DTO
"""

from pydantic import BaseModel, ConfigDict


class AIRequestDTO(BaseModel):

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    provider: str

    model: str

    prompt: str

    temperature: float

    max_tokens: int