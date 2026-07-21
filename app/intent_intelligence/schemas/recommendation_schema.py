from pydantic import BaseModel, Field

from app.intent_intelligence.enums.engagement_strategy import (
    EngagementStrategy,
)

from app.intent_intelligence.enums.recommendation_type import (
    RecommendationType,
)

from app.intent_intelligence.schemas.reasoning_schema import (
    Reasoning,
)


class Recommendation(BaseModel):
    """
    Recommended engagement for the customer.
    """

    title: str

    description: str

    recommendation_type: RecommendationType

    engagement_strategy: EngagementStrategy

    confidence: float = Field(
        ge=0,
        le=1,
    )

    estimated_value: float | None = None

    reasoning: Reasoning