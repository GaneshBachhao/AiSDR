"""
Pain Point Extractor
"""

from app.intelligence.common.extractors.base_extractor import (
    BaseExtractor,
)


class PainPointExtractor(BaseExtractor):

    PAINS = [

        "manual",

        "slow",

        "delay",

        "repetitive",

        "inefficient",

        "expensive",

        "high cost",

        "legacy",

        "too many emails",

    ]

    def extract(
        self,
        text: str,
    ):

        normalized = self.normalize(text)

        evidence = []

        for pain in self.PAINS:

            if pain in normalized:

                evidence.append(

                    self.build_evidence(

                        category="Pain Point",

                        source=self.__class__.__name__,

                        text=pain,

                    )

                )

        return evidence