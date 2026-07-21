"""
Keyword Extractor
"""

from app.intelligence.common.extractors.base_extractor import (
    BaseExtractor,
)


class KeywordExtractor(BaseExtractor):

    KEYWORDS = [

        "automation",

        "workflow",

        "crm",

        "sales",

        "support",

        "manual",

        "approval",

        "invoice",

        "chatbot",

        "ai",

        "process",

        "digital transformation",

    ]

    def extract(
        self,
        text: str,
    ):

        normalized = self.normalize(text)

        evidence = []

        for keyword in self.KEYWORDS:

            if keyword in normalized:

                evidence.append(

                    self.build_evidence(

                        category="Keyword",

                        source=self.__class__.__name__,

                        text=keyword,

                    )

                )

        return evidence