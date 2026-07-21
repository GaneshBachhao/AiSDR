"""
Scoring Service
"""

from app.intelligence.base.base_service import (

    BaseService,

)

from app.intelligence.pipelines.scoring_pipeline import (

    ScoringPipeline,

)


class ScoringService(
    BaseService,
):
    """
    Enterprise scoring service.
    """

    def __init__(self):

        super().__init__()

        self.pipeline = ScoringPipeline()

    def score(

        self,

        evidence,

    ):

        self.log_info(

            "Running scoring pipeline.",

        )

        return self.pipeline.score(

            evidence,

        )