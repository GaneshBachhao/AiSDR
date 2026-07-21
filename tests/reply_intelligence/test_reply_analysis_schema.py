from app.reply_intelligence.schemas.reply_analysis_schema import ReplyAnalysis
from app.reply_intelligence.enums.reply_intent import ReplyIntent
from app.reply_intelligence.enums.sentiment import Sentiment


def test_reply_analysis():

    analysis = ReplyAnalysis(
        intent=ReplyIntent.INTERESTED,
        sentiment=Sentiment.POSITIVE,
        confidence=0.96,
        meeting_requested=False,
        needs_followup=True,
        reason="Interested in learning more.",
    )

    assert analysis.intent == ReplyIntent.INTERESTED
    assert analysis.sentiment == Sentiment.POSITIVE
    assert analysis.confidence == 0.96