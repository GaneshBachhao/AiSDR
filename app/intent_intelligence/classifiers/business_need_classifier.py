"""
Business Need Classifier
"""

from app.intent_intelligence.classifiers.base_classifier import (
    BaseClassifier,
)

from app.intent_intelligence.enums.business_need import (
    BusinessNeed,
)


class BusinessNeedClassifier(BaseClassifier):

    KEYWORDS = {

        BusinessNeed.AUTOMATION: [
            "automation",
            "automate",
            "workflow",
            "manual",
        ],

        BusinessNeed.CUSTOMER_SUPPORT: [
            "support",
            "customer",
            "ticket",
            "service desk",
        ],

        BusinessNeed.SALES: [
            "sales",
            "lead",
            "prospect",
            "crm",
        ],

        BusinessNeed.HR: [
            "hr",
            "recruitment",
            "employee",
        ],

        BusinessNeed.FINANCE: [
            "finance",
            "invoice",
            "payment",
        ],

        BusinessNeed.AI_STRATEGY: [
            "strategy",
            "roadmap",
            "consulting",
        ],
    }

    def classify(
        self,
        text: str,
    ) -> BusinessNeed:

        text = text.lower()

        for need, keywords in self.KEYWORDS.items():

            if any(
                keyword in text
                for keyword in keywords
            ):
                return need

        return BusinessNeed.UNKNOWN