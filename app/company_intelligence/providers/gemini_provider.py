"""
Gemini Company Intelligence Provider
"""

from app.core.logger import logger

from app.company_intelligence.parsers.company_profile_parser import (
    CompanyProfileParser,
)
from app.company_intelligence.prompts.enrichment_prompt import (
    EnrichmentPrompt,
)
from app.company_intelligence.providers.base_provider import (
    BaseCompanyIntelligenceProvider,
)
from app.company_intelligence.schemas.company_profile_schema import (
    CompanyProfile,
)
from app.integrations.llm.provider_factory import (
    LLMProviderFactory,
)
from app.lead_intelligence.schemas.lead_candidate_schema import (
    LeadCandidate,
)
from app.exceptions.custom_exceptions import (
    GeminiGenerationException,
)


class GeminiCompanyIntelligenceProvider(
    BaseCompanyIntelligenceProvider
):
    """
    Enriches a LeadCandidate using Gemini.
    """

    def __init__(
        self,
        client=None,
    ):
        """
        Client is lazily created.

        Tests can inject a fake client to avoid
        importing the Gemini SDK.
        """

        self.client = client

    @property
    def llm(self):
        """
        Lazily create the LLM client only when needed.
        """

        if self.client is None:
            self.client = LLMProviderFactory.get_client()

        return self.client

    def enrich(
        self,
        candidate: LeadCandidate,
    ) -> CompanyProfile:

        try:

            prompt = EnrichmentPrompt.build(candidate)

            response = self.llm.generate(
                prompt=prompt,
                temperature=0.0,
            )

            profile = CompanyProfileParser.parse(
                response.text,
            )

            if not profile.company_name:
                raise ValueError(
                    "Company name missing in AI response."
                )

            logger.info(
                f"Company enrichment succeeded: "
                f"{profile.company_name}"
            )

            return profile

        except (
            GeminiGenerationException,
            ValueError,
        ) as ex:

            logger.warning(
                f"Company enrichment fallback for "
                f"{candidate.company_name}: {ex}"
            )

        except Exception:

            logger.exception(
                f"Unexpected enrichment failure for "
                f"{candidate.company_name}"
            )

        return CompanyProfile(
            company_name=candidate.company_name,
            website=str(candidate.website)
            if candidate.website
            else None,
            industry=candidate.industry,
            country=candidate.country,
            state=candidate.state,
            city=candidate.city,
            employee_count=candidate.employee_count,
        )