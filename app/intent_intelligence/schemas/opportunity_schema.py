from pydantic import BaseModel, Field

from app.intent_intelligence.enums.opportunity_type import (
    OpportunityType,
)

from app.intent_intelligence.schemas.recommendation_schema import (
    Recommendation,
)


class Opportunity(BaseModel):
    """
    Business opportunity discovered by AI.
    """

    opportunity_type: OpportunityType

    title: str

    description: str

    score: float = Field(
        ge=0,
        le=100,
    )

    recommendations: list[Recommendation] = Field(
        default_factory=list,
    )