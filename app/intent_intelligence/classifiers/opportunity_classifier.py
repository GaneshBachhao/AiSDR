"""
Opportunity Classifier
"""

from app.intent_intelligence.enums.business_need import (
    BusinessNeed,
)

from app.intent_intelligence.enums.buying_stage import (
    BuyingStage,
)

from app.intent_intelligence.enums.urgency_level import (
    UrgencyLevel,
)


class OpportunityClassifier:
    """
    Calculates an opportunity score.
    """

    def classify(
        self,
        business_need: BusinessNeed,
        buying_stage: BuyingStage,
        urgency: UrgencyLevel,
    ) -> float:

        score = 0.0

        # Buying stage contribution

        stage_scores = {

            BuyingStage.AWARENESS: 20,

            BuyingStage.RESEARCH: 35,

            BuyingStage.EVALUATION: 60,

            BuyingStage.SHORTLIST: 80,

            BuyingStage.NEGOTIATION: 90,

            BuyingStage.READY_TO_BUY: 100,

            BuyingStage.EXISTING_CUSTOMER: 50,

            BuyingStage.UNKNOWN: 10,
        }

        score += stage_scores.get(
            buying_stage,
            10,
        )

        # Urgency contribution

        urgency_bonus = {

            UrgencyLevel.LOW: 0,

            UrgencyLevel.MEDIUM: 5,

            UrgencyLevel.HIGH: 10,

            UrgencyLevel.CRITICAL: 20,
        }

        score += urgency_bonus.get(
            urgency,
            0,
        )

        # Strategic business needs

        strategic_needs = {

            BusinessNeed.AI_STRATEGY,

            BusinessNeed.AUTOMATION,

            BusinessNeed.DIGITAL_TRANSFORMATION,
        }

        if business_need in strategic_needs:

            score += 10

        return min(
            score,
            100,
        )