"""
Extraction Pipeline

Runs every registered extractor and
collects Evidence objects.
"""

from app.intelligence.common.schemas import (
    Evidence,
)

from app.intelligence.registry import (
    ExtractorRegistry,
)


class ExtractionPipeline:
    """
    Enterprise extraction pipeline.
    """

    def __init__(self):

        self.extractors = (
            ExtractorRegistry.get_extractors()
        )

    def extract(
        self,
        text: str,
    ) -> list[Evidence]:

        evidence = []

        for extractor in self.extractors:

            evidence.extend(

                extractor.extract(text)

            )

        return evidence