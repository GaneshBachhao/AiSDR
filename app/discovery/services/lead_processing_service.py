"""
Lead Processing Service

Processes discovered companies through the SDR pipeline.
"""

from __future__ import annotations

from app.pipelines.orchestrator import (
    PipelineOrchestrator,
)

from app.pipelines.stages.company_intelligence_stage import (
    CompanyIntelligenceStage,
)

from app.pipelines.stages.qualification_stage import (
    QualificationStage,
)

from app.pipelines.stages.lead_creation_stage import (
    LeadCreationStage,
)


class LeadProcessingService:
    """
    Executes the lead processing pipeline.

    Converts discovered companies into qualified leads.
    """

    def __init__(self) -> None:

        self._orchestrator = PipelineOrchestrator(
            stages=[
                CompanyIntelligenceStage(),
                QualificationStage(),
                LeadCreationStage(),
            ]
        )