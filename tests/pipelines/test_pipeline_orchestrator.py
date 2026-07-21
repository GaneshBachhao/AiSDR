"""
Tests for PipelineOrchestrator.
"""

from app.pipelines.context.pipeline_context import PipelineContext
from app.pipelines.orchestrator import PipelineOrchestrator
from app.pipelines.stages.base_stage import BasePipelineStage


class DummyStage(BasePipelineStage):

    @property
    def stage_name(self) -> str:
        return self.__class__.__name__

    def execute(
        self,
        context: PipelineContext,
    ) -> PipelineContext:

        return context


def test_pipeline_executes_all_stages():

    context = PipelineContext()

    orchestrator = PipelineOrchestrator(

        stages=[
            DummyStage(),
            DummyStage(),
            DummyStage(),
        ]

    )

    result = orchestrator.execute(context)

    assert result.completed_stages == [
        "DummyStage",
        "DummyStage",
        "DummyStage",
    ]

    assert result.current_stage == "DummyStage"

    assert result.status == "COMPLETED"