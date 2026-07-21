"""
Technology Extractor
"""

from app.intelligence.common.extractors.base_extractor import (
    BaseExtractor,
)


class TechnologyExtractor(BaseExtractor):

    TECHNOLOGIES = [

        "aws",

        "azure",

        "gcp",

        "microsoft 365",

        "google workspace",

        "salesforce",

        "hubspot",

        "oracle",

        "sap",

        "postgresql",

        "mysql",

        "python",

        "fastapi",

        "docker",

        "kubernetes",

    ]

    def extract(
        self,
        text: str,
    ):

        normalized = self.normalize(text)

        evidence = []

        for tech in self.TECHNOLOGIES:

            if tech in normalized:

                evidence.append(

                    self.build_evidence(

                        category="Technology",

                        source=self.__class__.__name__,

                        text=tech,

                    )

                )

        return evidence