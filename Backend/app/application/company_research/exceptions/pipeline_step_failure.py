"""
Internal control-flow exception used only within ``SearchCompaniesHandler``
to tag *which* pipeline step an unexpected failure happened in, before it's
converted into a ``CandidateResearchFailure`` for the caller. Never expected
to propagate past that handler -- it exists so the outer per-candidate
exception boundary doesn't have to guess where the exception came from.
"""

from __future__ import annotations

from app.domain.company_research.value_objects.pipeline_step import PipelineStep


class PipelineStepFailure(Exception):
    def __init__(self, step: PipelineStep, message: str) -> None:
        self.step = step
        super().__init__(message)
