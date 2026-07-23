"""
Company Profile Mapper

Maps between Application objects and
Company Intelligence schemas.
"""

from app.application.company_intelligence.commands.enrich_company import (
    EnrichCompanyCommand,
)

from app.application.company_intelligence.dto.enrich_company_request_dto import (
    EnrichCompanyRequestDTO,
)

from app.application.company_intelligence.dto.enrich_company_response_dto import (
    EnrichCompanyResponseDTO,
)

from app.company_intelligence.schemas.company_profile_schema import (
    CompanyProfile,
)

from app.lead_intelligence.schemas.lead_candidate_schema import (
    LeadCandidate,
)


class CompanyProfileMapper:
    """
    Mapper for Company Intelligence.
    """

    @staticmethod
    def command_to_dto(
        command: EnrichCompanyCommand,
    ) -> EnrichCompanyRequestDTO:

        return EnrichCompanyRequestDTO(

            company_name=command.company_name,

            website=command.website,

            industry=command.industry,

            country=command.country,

            state=command.state,

            city=command.city,

            linkedin_url=command.linkedin_url,

            phone=command.phone,

            email=command.email,

            employee_count=command.employee_count,

            source=command.source,

            confidence=command.confidence,

            metadata=command.metadata,
        )

    @staticmethod
    def dto_to_candidate(
        dto: EnrichCompanyRequestDTO,
    ) -> LeadCandidate:

        return LeadCandidate(

            company_name=dto.company_name,

            website=dto.website,

            industry=dto.industry,

            country=dto.country,

            state=dto.state,

            city=dto.city,

            linkedin_url=dto.linkedin_url,

            phone=dto.phone,

            email=dto.email,

            employee_count=dto.employee_count,

            source=dto.source,

            confidence=dto.confidence,

            metadata=dto.metadata,
        )

    @staticmethod
    def profile_to_response(
        profile: CompanyProfile,
    ) -> EnrichCompanyResponseDTO:

        return EnrichCompanyResponseDTO(

            company_name=profile.company_name,

            website=profile.website,

            linkedin_url=profile.linkedin_url,

            country=profile.country,

            state=profile.state,

            city=profile.city,

            industry=profile.industry,

            description=profile.description,

            employee_count=profile.employee_count,

            estimated_revenue=profile.estimated_revenue,

            products=profile.products,

            services=profile.services,

            technologies=profile.technologies,

            certifications=profile.certifications,

            ai_readiness=profile.ai_readiness,

            confidence=profile.confidence,

            source=profile.source,

            metadata=profile.metadata,
        )