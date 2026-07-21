"""
Goal Extractor
"""

from app.intelligence.common.extractors.base_extractor import (
    BaseExtractor,
)


class GoalExtractor(BaseExtractor):

    GOALS = [

        "increase sales",

        "reduce cost",

        "save time",

        "automation",

        "improve efficiency",

        "digital transformation",

        "growth",

        "scale",

    ]

    def extract(
        self,
        text: str,
    ):

        normalized = self.normalize(text)

        evidence = []

        for goal in self.GOALS:

            if goal in normalized:

                evidence.append(

                    self.build_evidence(

                        category="Business Goal",

                        source=self.__class__.__name__,

                        text=goal,

                    )

                )

        return evidence