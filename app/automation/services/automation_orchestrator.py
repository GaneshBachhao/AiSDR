"""
Automation Orchestrator

Coordinates reply intelligence with the automation framework.
"""

from sqlalchemy.orm import Session

from app.automation.rules.reply_rules import (
    ReplyRules,
)

from app.automation.workflows.workflow_executor import (
    WorkflowExecutor,
)

from app.reply_intelligence.schemas.reply_analysis_schema import (
    ReplyAnalysis,
)


class AutomationOrchestrator:
    """
    Coordinates the complete automation pipeline.
    """

    def __init__(
        self,
        executor: WorkflowExecutor | None = None,
    ):
        self.executor = (
            executor
            or WorkflowExecutor()
        )

    def process_reply(
        self,
        db: Session,
        analysis: ReplyAnalysis,
        lead_id: int,
        conversation_id: int,
    ) -> list[str]:
        """
        Process a customer reply.

        1. Build automation workflow.
        2. Execute workflow.
        3. Return execution summary.
        """

        workflow = ReplyRules.determine_actions(

            analysis=analysis,

            lead_id=lead_id,

            conversation_id=conversation_id,
        )

        return self.executor.execute(
            db=db,
            result=workflow,
        )