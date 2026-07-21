"""
Entity Extractor
"""

from app.intelligence.common.extractors.base_extractor import (
    BaseExtractor,
)


class EntityExtractor(BaseExtractor):

    ENTITIES = [

        "microsoft",

        "google",

        "amazon",

        "salesforce",

        "hubspot",

        "oracle",

        "sap",

        "openai",

        "gemini",

        "claude",

    ]

    def extract(
        self,
        text: str,
    ):

        normalized = self.normalize(text)

        evidence = []

        for entity in self.ENTITIES:

            if entity in normalized:

                evidence.append(

                    self.build_evidence(

                        category="Entity",

                        source=self.__class__.__name__,

                        text=entity,

                    )

                )

        return evidence