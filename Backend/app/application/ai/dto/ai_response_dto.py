"""
AI Response DTO
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TokenUsageDTO(BaseModel):

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    prompt_tokens: int

    completion_tokens: int

    total_tokens: int


class AIResponseDTO(BaseModel):

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    response_id: str

    content: str

    finish_reason: str

    token_usage: TokenUsageDTO

    created_at: datetime