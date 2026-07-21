from app.company_intelligence.schemas.company_profile_schema import (
    CompanyProfile,
)

from app.integrations.llm.response import (
    LLMResponse,
)

from app.reply_intelligence.services.reply_analysis_service import (
    ReplyAnalysisService,
)


class FakeLLM:

    def generate(
        self,
        prompt,
        temperature=0.2,
        max_tokens=None,
    ):

        return LLMResponse(
            text="""
{
    "intent":"MEETING_REQUEST",
    "sentiment":"POSITIVE",
    "confidence":0.99,
    "meeting_requested":true,
    "needs_followup":false,
    "reason":"Customer requested a meeting."
}
""",
            provider="fake",
            model="fake",
            latency_ms=0,
        )


def test_reply_analysis():

    service = ReplyAnalysisService(
        llm=FakeLLM(),
    )

    company = CompanyProfile(
        company_name="ABC Manufacturing",
    )

    result = service.analyze(
        company,
        "Original Email",
        "Can we meet next week?",
    )

    assert result.meeting_requested is True
    assert result.intent.value == "MEETING_REQUEST"