"""
Enterprise Intelligence Context

Carries all information required by the
intelligence pipeline.
"""

from pydantic import BaseModel
from pydantic import Field

from app.intelligence.enums.source_type import SourceType


class IntelligenceContext(BaseModel):
    """
    Unified intelligence context.
    """

    source: SourceType

    raw_text: str

    lead_id: int | None = None

    company_id: int | None = None

    conversation_id: int | None = None

    campaign_id: int | None = None

    metadata: dict[str, str] = Field(
        default_factory=dict,
    )