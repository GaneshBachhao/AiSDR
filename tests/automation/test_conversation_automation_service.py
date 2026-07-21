from app.automation.enums.action_type import (
    ActionType,
)

from app.automation.services.conversation_automation_service import (
    ConversationAutomationService,
)

from app.leads.enums.lead_status import (
    LeadStatus,
)

from app.reply_intelligence.enums.reply_intent import (
    ReplyIntent,
)

from app.reply_intelligence.enums.sentiment import (
    Sentiment,
)

from app.reply_intelligence.schemas.reply_analysis_schema import (
    ReplyAnalysis,
)


def test_interested():

    service = ConversationAutomationService()

    analysis = ReplyAnalysis(

        intent=ReplyIntent.INTERESTED,

        sentiment=Sentiment.POSITIVE,

        confidence=0.95,

        meeting_requested=False,

        needs_followup=True,

        reason="Customer expressed interest.",
    )

    result = service.automate(

        analysis=analysis,

        lead_id=1,

        conversation_id=100,

    )

    assert result.success

    assert len(result.actions) == 3

    assert result.actions[0].action == ActionType.UPDATE_LEAD


def test_not_interested():

    service = ConversationAutomationService()

    analysis = ReplyAnalysis(

        intent=ReplyIntent.NOT_INTERESTED,

        sentiment=Sentiment.NEGATIVE,

        confidence=0.99,

        meeting_requested=False,

        needs_followup=False,

        reason="Customer declined.",
    )

    result = service.automate(

        analysis=analysis,

        lead_id=1,

        conversation_id=100,

    )

    assert result.success

    assert len(result.actions) == 1

    assert result.actions[0].action == ActionType.UPDATE_LEAD

    assert (
        result.actions[0].payload["status"]
        == LeadStatus.LOST
    )