from app.automation.services.automation_orchestrator import (
    AutomationOrchestrator,
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


def test_interested_reply_workflow(monkeypatch):

    #
    # Prevent database access
    #

    monkeypatch.setattr(
        "app.services.lead_service.LeadService.qualify",
        lambda self, db, lead_id: None,
    )

    analysis = ReplyAnalysis(

        intent=ReplyIntent.INTERESTED,

        sentiment=Sentiment.POSITIVE,

        confidence=0.98,

        meeting_requested=False,

        needs_followup=True,

        reason="Customer would like a demo.",
    )

    orchestrator = AutomationOrchestrator()

    executed = orchestrator.process_reply(

        db=None,

        analysis=analysis,

        lead_id=1,

        conversation_id=1,
    )

    assert "UPDATE_LEAD" in executed

    assert "NOTIFY_SALES" in executed

    assert "GENERATE_REPLY" in executed