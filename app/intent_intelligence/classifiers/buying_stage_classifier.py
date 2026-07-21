"""
Buying Stage Classifier
"""

from app.intent_intelligence.classifiers.base_classifier import (
    BaseClassifier,
)

from app.intent_intelligence.enums.buying_stage import (
    BuyingStage,
)


class BuyingStageClassifier(BaseClassifier):
    """
    Determines the customer's buying stage.
    """

    STAGES = {

        BuyingStage.AWARENESS: [
            "curious",
            "exploring",
            "learning",
            "researching",
            "heard about",
        ],

        BuyingStage.RESEARCH: [
            "looking for",
            "options",
            "compare",
            "information",
            "solution",
        ],

        BuyingStage.EVALUATION: [
            "evaluate",
            "demo",
            "assessment",
            "meeting",
            "discussion",
        ],

        BuyingStage.SHORTLIST: [
            "shortlist",
            "vendors",
            "proposal",
            "quotation",
        ],

        BuyingStage.NEGOTIATION: [
            "pricing",
            "contract",
            "discount",
            "commercial",
            "agreement",
        ],

        BuyingStage.READY_TO_BUY: [
            "start",
            "kickoff",
            "purchase",
            "go ahead",
            "move forward",
        ],

        BuyingStage.EXISTING_CUSTOMER: [
            "already customer",
            "existing customer",
            "renewal",
        ],
    }

    def classify(
        self,
        text: str,
    ) -> BuyingStage:

        text = text.lower()

        for stage, keywords in self.STAGES.items():

            if any(
                keyword in text
                for keyword in keywords
            ):
                return stage

        return BuyingStage.UNKNOWN