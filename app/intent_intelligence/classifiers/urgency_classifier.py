"""
Urgency Classifier
"""

from app.intent_intelligence.classifiers.base_classifier import (
    BaseClassifier,
)

from app.intent_intelligence.enums.urgency_level import (
    UrgencyLevel,
)


class UrgencyClassifier(BaseClassifier):
    """
    Determines urgency from customer reply.
    """

    LEVELS = {

        UrgencyLevel.CRITICAL: [
            "urgent",
            "immediately",
            "asap",
            "today",
            "critical",
        ],

        UrgencyLevel.HIGH: [
            "soon",
            "this week",
            "priority",
        ],

        UrgencyLevel.MEDIUM: [
            "next week",
            "this month",
            "planning",
        ],

        UrgencyLevel.LOW: [
            "future",
            "later",
            "next quarter",
            "next year",
        ],
    }

    def classify(
        self,
        text: str,
    ) -> UrgencyLevel:

        text = text.lower()

        for level, keywords in self.LEVELS.items():

            if any(
                keyword in text
                for keyword in keywords
            ):
                return level

        return UrgencyLevel.MEDIUM