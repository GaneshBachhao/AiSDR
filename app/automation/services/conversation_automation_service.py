"""
Conversation Automation Service

Converts reply analysis into automation actions.
"""

from app.automation.rules.reply_rules import (
    ReplyRules,
)

from app.automation.schemas.automation_result_schema import (
    AutomationResult,
)

from app.reply_intelligence.schemas.reply_analysis_schema import (
    ReplyAnalysis,
)


class ConversationAutomationService:
    """
    Builds automation actions from reply analysis.
    """

    def automate(
        self,
        analysis: ReplyAnalysis,
        lead_id: int,
        conversation_id: int,
    ) -> AutomationResult:
        """
        Determine automation actions.
        """

        return ReplyRules.determine_actions(
            analysis=analysis,
            lead_id=lead_id,
            conversation_id=conversation_id,
        )