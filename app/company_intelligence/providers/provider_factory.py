"""
Company Intelligence Provider Factory
"""

from app.company_intelligence.providers.base_provider import (
    BaseCompanyIntelligenceProvider,
)

from app.company_intelligence.providers.gemini_provider import (
    GeminiCompanyIntelligenceProvider,
)


class CompanyIntelligenceProviderFactory:
    """
    Returns the configured Company Intelligence Provider.
    """

    @staticmethod
    def get_provider() -> BaseCompanyIntelligenceProvider:

        return GeminiCompanyIntelligenceProvider()