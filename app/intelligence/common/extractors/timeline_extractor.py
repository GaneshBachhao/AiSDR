"""
Timeline Extractor
"""

from app.intelligence.common.extractors.base_extractor import (
    BaseExtractor,
)


class TimelineExtractor(BaseExtractor):

    TERMS = [

        "today",

        "tomorrow",

        "next week",

        "next month",

        "this quarter",

        "next quarter",

        "asap",

        "immediately",

    ]

    def extract(
        self,
        text: str,
    ):

        normalized = self.normalize(text)

        evidence = []

        for term in self.TERMS:

            if term in normalized:

                evidence.append(

                    self.build_evidence(

                        category="Timeline",

                        source=self.__class__.__name__,

                        text=term,

                    )

                )

        return evidence