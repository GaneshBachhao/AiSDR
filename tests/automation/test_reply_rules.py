"""
Tests for ReplyRules.
"""

from app.automation.enums.action_type import (
    ActionType,
)

from app.automation.rules.reply_rules import (
    ReplyRules,
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

    analysis = ReplyAnalysis(

        intent=ReplyIntent.INTERESTED,

        sentiment=Sentiment.POSITIVE,

        confidence=0.95,

        meeting_requested=False,

        needs_followup=True,

        reason="Interested",
    )

    result = ReplyRules.determine_actions(

        analysis=analysis,

        lead_id=1,

        conversation_id=10,

    )

    assert len(result.actions) == 3

    assert result.actions[0].action == ActionType.UPDATE_LEAD


def test_not_interested():

    analysis = ReplyAnalysis(

        intent=ReplyIntent.NOT_INTERESTED,

        sentiment=Sentiment.NEGATIVE,

        confidence=0.99,

        meeting_requested=False,

        needs_followup=False,

        reason="Declined",
    )

    result = ReplyRules.determine_actions(

        analysis=analysis,

        lead_id=1,

        conversation_id=10,

    )

    assert len(result.actions) == 1

    assert result.actions[0].action == ActionType.UPDATE_LEAD

    assert (
        result.actions[0].payload["status"]
        == LeadStatus.LOST
    )


def test_unknown():

    analysis = ReplyAnalysis(

        intent=ReplyIntent.UNKNOWN,

        sentiment=Sentiment.NEUTRAL,

        confidence=0.10,

        meeting_requested=False,

        needs_followup=False,

        reason="Unknown",
    )

    result = ReplyRules.determine_actions(

        analysis=analysis,

        lead_id=1,

        conversation_id=10,

    )

    assert len(result.actions) == 1

    assert result.actions[0].action == ActionType.NO_ACTION