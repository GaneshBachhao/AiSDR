"""
Conversation Schemas
"""

from datetime import datetime

from pydantic import BaseModel

from app.conversations.enums.conversation_status import (
    ConversationStatus,
)


class ConversationCreate(BaseModel):

    lead_id: int

    contact_id: int

    provider: str = "gmail"

    provider_thread_id: str


class ConversationUpdate(BaseModel):

    status: ConversationStatus | None = None

    last_message_at: datetime | None = None

    closed_at: datetime | None = None


class ConversationResponse(BaseModel):

    id: int

    lead_id: int

    contact_id: int

    provider: str

    provider_thread_id: str

    status: ConversationStatus

    started_at: datetime

    last_message_at: datetime | None = None

    closed_at: datetime | None = None

    class Config:

        from_attributes = True