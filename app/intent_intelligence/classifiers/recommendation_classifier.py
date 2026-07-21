"""
Recommendation Classifier
"""

from app.intent_intelligence.enums.business_need import (
    BusinessNeed,
)

from app.intent_intelligence.enums.engagement_strategy import (
    EngagementStrategy,
)

from app.intent_intelligence.enums.recommendation_type import (
    RecommendationType,
)

from app.intent_intelligence.schemas.reasoning_schema import (
    Reasoning,
)

from app.intent_intelligence.schemas.recommendation_schema import (
    Recommendation,
)


class RecommendationClassifier:
    """
    Generates consulting recommendations.
    """

    def classify(
        self,
        business_need: BusinessNeed,
    ) -> list[Recommendation]:

        recommendations = {

            BusinessNeed.AUTOMATION: Recommendation(

                title="AI Process Automation Assessment",

                description="Identify automation opportunities across business workflows.",

                recommendation_type=RecommendationType.ASSESSMENT,

                engagement_strategy=EngagementStrategy.AI_ASSESSMENT,

                confidence=0.95,

                estimated_value=10000,

                reasoning=Reasoning(

                    confidence=0.95,

                    explanation="Customer expressed automation interest.",
                ),
            ),

            BusinessNeed.AI_STRATEGY: Recommendation(

                title="AI Readiness Assessment",

                description="Evaluate AI maturity and prepare roadmap.",

                recommendation_type=RecommendationType.CONSULTATION
                if hasattr(RecommendationType, "CONSULTATION")
                else RecommendationType.SERVICE,

                engagement_strategy=EngagementStrategy.CONSULTATION,

                confidence=0.97,

                estimated_value=15000,

                reasoning=Reasoning(

                    confidence=0.97,

                    explanation="Customer requested AI strategy guidance.",
                ),
            ),

            BusinessNeed.CUSTOMER_SUPPORT: Recommendation(

                title="AI Customer Support Solution",

                description="Deploy AI chatbot and agent assist platform.",

                recommendation_type=RecommendationType.SERVICE,

                engagement_strategy=EngagementStrategy.DEMO,

                confidence=0.92,

                estimated_value=12000,

                reasoning=Reasoning(

                    confidence=0.92,

                    explanation="Support automation opportunity detected.",
                ),
            ),
        }

        recommendation = recommendations.get(
            business_need,
        )

        if recommendation:

            return [recommendation]

        return []