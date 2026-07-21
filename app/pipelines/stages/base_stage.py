"""
Base Pipeline Stage

Defines the contract implemented by all
pipeline stages.
"""

from abc import ABC, abstractmethod

from app.pipelines.context.pipeline_context import (
    PipelineContext,
)


class BasePipelineStage(ABC):
    """
    Base class for all pipeline stages.

    Each stage receives a PipelineContext,
    performs a single responsibility, updates
    the context, and returns it.
    """

    @property
    @abstractmethod
    def stage_name(self) -> str:
        """
        Human-readable stage name.

        Used for logging, monitoring,
        dashboards, and execution history.
        """
        raise NotImplementedError

    def can_execute(
        self,
        context: PipelineContext,
    ) -> bool:
        """
        Determines whether this stage should
        execute.

        Stages may override this to skip
        execution based on the current
        PipelineContext.

        Default:
            Always execute.
        """
        return True

    @abstractmethod
    def execute(
        self,
        context: PipelineContext,
    ) -> PipelineContext:
        """
        Execute the pipeline stage.

        Args:
            context:
                Shared pipeline context.

        Returns:
            Updated PipelineContext.
        """
        raise NotImplementedError

    def after_execute(
        self,
        context: PipelineContext,
    ) -> None:
        """
        Optional hook executed after a
        successful stage execution.

        Override only when required.

        Default:
            No operation.
        """
        return