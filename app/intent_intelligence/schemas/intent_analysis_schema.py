from pydantic import BaseModel, Field

from app.intent_intelligence.enums.business_need import (
    BusinessNeed,
)

from app.intent_intelligence.enums.buying_stage import (
    BuyingStage,
)

from app.intent_intelligence.enums.budget_indicator import (
    BudgetIndicator,
)

from app.intent_intelligence.enums.decision_authority import (
    DecisionAuthority,
)

from app.intent_intelligence.enums.urgency_level import (
    UrgencyLevel,
)

from app.intent_intelligence.schemas.opportunity_schema import (
    Opportunity,
)

from app.reply_intelligence.schemas.reply_analysis_schema import (
    ReplyAnalysis,
)


class IntentAnalysis(BaseModel):
    """
    Rich business understanding produced by
    the Intent Intelligence Engine.
    """

    reply_analysis: ReplyAnalysis

    business_need: BusinessNeed

    buying_stage: BuyingStage

    urgency: UrgencyLevel

    budget: BudgetIndicator

    decision_authority: DecisionAuthority

    opportunity_score: float = Field(
        ge=0,
        le=100,
    )

    pain_points: list[str] = Field(
        default_factory=list,
    )

    business_goals: list[str] = Field(
        default_factory=list,
    )

    opportunities: list[Opportunity] = Field(
        default_factory=list,
    )

    next_actions: list[str] = Field(
        default_factory=list,
    )