from pydantic import BaseModel, Field

from app.reply_intelligence.enums.reply_intent import ReplyIntent
from app.reply_intelligence.enums.sentiment import Sentiment


class ReplyAnalysis(BaseModel):
    """
    Structured result returned by the AI reply analysis.
    """

    intent: ReplyIntent

    sentiment: Sentiment

    confidence: float = Field(
        ge=0,
        le=1,
    )

    meeting_requested: bool = False

    needs_followup: bool = False

    reason: str