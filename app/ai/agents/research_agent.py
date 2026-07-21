from app.ai.prompts.research_prompt import build_company_research_prompt
from app.ai.services.ai_service import AIService


class ResearchAgent:
    """
    AI agent responsible for researching a company
    using the configured LLM provider.
    """

    def __init__(self):
        self.ai_service = AIService()

    def research_company(
        self,
        company_name: str,
        website: str | None = None,
    ) -> dict:
        """
        Research a company and return structured JSON.
        """

        prompt = build_company_research_prompt(
            company_name=company_name,
            website=website,
        )

        return self.ai_service.generate(prompt)