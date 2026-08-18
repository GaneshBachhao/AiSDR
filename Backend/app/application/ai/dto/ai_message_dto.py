"""
AI Message DTO
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AIMessageDTO(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    role: str

    content: str

    created_at: datetime
