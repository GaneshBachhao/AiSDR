"""
Extractor Registry

Registers all extractors used by the
Enterprise Intelligence Framework.
"""

from app.intelligence.common.extractors import (
    EntityExtractor,
    GoalExtractor,
    KeywordExtractor,
    PainPointExtractor,
    TechnologyExtractor,
    TimelineExtractor,
)


class ExtractorRegistry:
    """
    Registry of available extractors.
    """

    @staticmethod
    def get_extractors():

        return [

            KeywordExtractor(),

            EntityExtractor(),

            TimelineExtractor(),

            PainPointExtractor(),

            GoalExtractor(),

            TechnologyExtractor(),

        ]