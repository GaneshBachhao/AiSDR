"""
Pipeline Orchestrator

Executes a sequence of pipeline stages.
"""

import time
from datetime import datetime, UTC

from app.core.logger import logger

from app.pipelines.context.pipeline_context import (
    PipelineContext,
)

from app.pipelines.stages.base_stage import (
    BasePipelineStage,
)


class PipelineOrchestrator:
    """
    Executes pipeline stages sequentially.

    The orchestrator owns the execution lifecycle,
    including timing, stage tracking, logging,
    and pipeline status.
    """

    def __init__(
        self,
        stages: list[BasePipelineStage],
    ):
        self.stages = stages

    def execute(
        self,
        context: PipelineContext,
    ) -> PipelineContext:

        start_time = time.perf_counter()

        logger.info("=" * 80)
        logger.info(
            f"Pipeline Started | "
            f"Execution={context.execution_id}"
        )
        logger.info("=" * 80)

        try:

            for stage in self.stages:

                if not stage.can_execute(context):

                    logger.info(
                        f"Skipping Stage : "
                        f"{stage.stage_name}"
                    )

                    continue

                logger.info(
                    f"Executing Stage : "
                    f"{stage.stage_name}"
                )

                context.current_stage = (
                    stage.stage_name
                )

                context = stage.execute(
                    context
                )

                stage.after_execute(
                    context
                )

                context.completed_stages.append(
                    stage.stage_name
                )

            context.status = "COMPLETED"

        except Exception as ex:

            context.status = "FAILED"

            context.errors.append(
                str(ex)
            )

            logger.exception(
                f"Pipeline failed during "
                f"{context.current_stage}"
            )

            raise

        finally:

            context.finished_at = (
                datetime.now(UTC)
            )

            context.duration_ms = (
                time.perf_counter() - start_time
            ) * 1000

            logger.info("=" * 80)
            logger.info(
                f"Pipeline Finished | "
                f"Status={context.status} | "
                f"Execution={context.execution_id} | "
                f"Duration={context.duration_ms:.0f} ms"
            )
            logger.info("=" * 80)

        return context