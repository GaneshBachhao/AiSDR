"""
Intent Intelligence Service

Coordinates all business intelligence classifiers.
"""

from app.intent_intelligence.classifiers.business_need_classifier import (
    BusinessNeedClassifier,
)

from app.intent_intelligence.classifiers.buying_stage_classifier import (
    BuyingStageClassifier,
)

from app.intent_intelligence.classifiers.urgency_classifier import (
    UrgencyClassifier,
)

from app.intent_intelligence.classifiers.opportunity_classifier import (
    OpportunityClassifier,
)

from app.intent_intelligence.classifiers.recommendation_classifier import (
    RecommendationClassifier,
)

from app.intent_intelligence.enums.budget_indicator import (
    BudgetIndicator,
)

from app.intent_intelligence.enums.decision_authority import (
    DecisionAuthority,
)

from app.intent_intelligence.schemas.intent_analysis_schema import (
    IntentAnalysis,
)

from app.reply_intelligence.schemas.reply_analysis_schema import (
    ReplyAnalysis,
)


class IntentIntelligenceService:
    """
    Builds a complete IntentAnalysis from ReplyAnalysis.
    """

    def __init__(self):

        self.business_classifier = (
            BusinessNeedClassifier()
        )

        self.buying_classifier = (
            BuyingStageClassifier()
        )

        self.urgency_classifier = (
            UrgencyClassifier()
        )

        self.opportunity_classifier = (
            OpportunityClassifier()
        )

        self.recommendation_classifier = (
            RecommendationClassifier()
        )

    def analyze(
        self,
        analysis: ReplyAnalysis,
    ) -> IntentAnalysis:
        """
        Produce a rich business understanding.
        """

        text = analysis.reason or ""

        business_need = (
            self.business_classifier.classify(
                text,
            )
        )

        buying_stage = (
            self.buying_classifier.classify(
                text,
            )
        )

        urgency = (
            self.urgency_classifier.classify(
                text,
            )
        )

        score = (
            self.opportunity_classifier.classify(
                business_need,
                buying_stage,
                urgency,
            )
        )

        recommendations = (
            self.recommendation_classifier.classify(
                business_need,
            )
        )

        return IntentAnalysis(

            reply_analysis=analysis,

            business_need=business_need,

            buying_stage=buying_stage,

            urgency=urgency,

            budget=BudgetIndicator.UNKNOWN,

            decision_authority=DecisionAuthority.UNKNOWN,

            opportunity_score=score,

            opportunities=[],

            next_actions=[
                r.title
                for r in recommendations
            ],

            pain_points=[],

            business_goals=[],
        )