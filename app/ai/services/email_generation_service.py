"""
AI Email Generation Service
"""

from app.ai.prompts.email_prompt_builder import (
    EmailPromptBuilder,
)

from app.ai.schemas.generated_email_schema import (
    GeneratedEmail,
)

from app.company_intelligence.schemas.company_profile_schema import (
    CompanyProfile,
)

from app.contacts.schemas.contact_schema import (
    ContactCreate,
)

from app.integrations.llm.base_client import (
    BaseLLMClient,
)

from app.integrations.llm.gemini_client import (
    GeminiClient,
)

from app.recommendation.schemas.recommendation_schema import (
    RecommendationResponse,
)


class EmailGenerationService:
    """
    Generates personalized outreach emails.
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

    def generate(
        self,
        company: CompanyProfile,
        contact: ContactCreate,
        recommendations: RecommendationResponse,
    ) -> GeneratedEmail:

        prompt = EmailPromptBuilder.build(
            company,
            contact,
            recommendations,
        )

        response = self.llm.generate(
            prompt,
        )

        return self._parse(
            response.text,
        )

    @staticmethod
    def _parse(
        text: str,
    ) -> GeneratedEmail:

        subject = ""
        body = ""

        lines = text.splitlines()

        in_body = False

        for line in lines:

            stripped = line.strip()

            if stripped.lower().startswith(
                "subject:"
            ):

                subject = stripped.replace(
                    "Subject:",
                    "",
                ).strip()

                continue

            if stripped.lower().startswith(
                "body:"
            ):

                in_body = True

                continue

            if in_body:

                body += line + "\n"

        return GeneratedEmail(
            subject=subject,
            body=body.strip(),
        )