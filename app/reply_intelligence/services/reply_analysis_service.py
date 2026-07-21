"""
Reply Analysis Service
"""

from app.company_intelligence.schemas.company_profile_schema import (
    CompanyProfile,
)

from app.integrations.llm.base_client import (
    BaseLLMClient,
)

from app.integrations.llm.gemini_client import (
    GeminiClient,
)

from app.reply_intelligence.parser.reply_parser import (
    ReplyParser,
)

from app.reply_intelligence.prompts.reply_analysis_prompt import (
    ReplyAnalysisPromptBuilder,
)

from app.reply_intelligence.schemas.reply_analysis_schema import (
    ReplyAnalysis,
)


class ReplyAnalysisService:
    """
    Uses an LLM to analyze customer replies.
    """

    def __init__(
        self,
        llm: BaseLLMClient | None = None,
    ):
        self.llm = (
            llm
            if llm is not None
            else GeminiClient()
        )

    def analyze(
        self,
        company: CompanyProfile,
        original_email: str,
        reply: str,
    ) -> ReplyAnalysis:

        prompt = ReplyAnalysisPromptBuilder.build(
            company=company,
            original_email=original_email,
            reply=reply,
        )

        response = self.llm.generate(
            prompt,
        )

        return ReplyParser.parse(
            response.text,
        )