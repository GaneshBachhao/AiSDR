"""
Reasoning Service
"""

from app.intelligence.base.base_service import (
    BaseService,
)

from app.intelligence.pipelines.reasoning_pipeline import (
    ReasoningPipeline,
)

from app.intelligence.common.schemas import (
    IntelligenceReport,
)


class ReasoningService(
    BaseService,
):
    """
    Enterprise reasoning service.
    """

    def __init__(self):

        super().__init__()

        self.pipeline = (
            ReasoningPipeline()
        )

    def reason(
        self,
        report: IntelligenceReport,
    ) -> IntelligenceReport:

        self.log_info(

            "Running reasoning pipeline."

        )

        return self.pipeline.run(
            report,
        )