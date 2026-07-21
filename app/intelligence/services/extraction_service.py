"""
Extraction Service

High-level service wrapping the
Extraction Pipeline.
"""

from app.intelligence.base.base_service import (
    BaseService,
)

from app.intelligence.pipelines import (
    ExtractionPipeline,
)


class ExtractionService(
    BaseService,
):
    """
    Enterprise extraction service.
    """

    def __init__(self):

        super().__init__()

        self.pipeline = (
            ExtractionPipeline()
        )

    def extract(
        self,
        text: str,
    ):

        self.log_info(
            "Running extraction pipeline."
        )

        return self.pipeline.extract(
            text,
        )