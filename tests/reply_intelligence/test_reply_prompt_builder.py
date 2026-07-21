from app.reply_intelligence.prompts.reply_analysis_prompt import (
    ReplyAnalysisPromptBuilder,
)

from app.company_intelligence.schemas.company_profile_schema import (
    CompanyProfile,
)


def test_prompt_contains_company():

    company = CompanyProfile(
        company_name="ABC Manufacturing",
        industry="Manufacturing",
    )

    prompt = ReplyAnalysisPromptBuilder.build(
        company,
        "Original email",
        "Looks interesting.",
    )

    assert "ABC Manufacturing" in prompt
    assert "Looks interesting." in prompt
    assert "Return ONLY valid JSON" in prompt