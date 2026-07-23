"""
Discovery Mapper

Maps between Application objects and Discovery schemas.
"""

from app.application.discovery.commands.discover_companies import (
    DiscoverCompaniesCommand,
)

from app.application.discovery.dto.discovery_request_dto import (
    DiscoveryRequestDTO,
)

from app.application.discovery.dto.discovery_response_dto import (
    DiscoveryCompanyDTO,
    DiscoveryResponseDTO,
)

from app.discovery.schemas.discovery_schema import (
    DiscoveryRequest,
    DiscoveryResult,
)


class DiscoveryMapper:
    """
    Mapper for Discovery module.
    """

    @staticmethod
    def command_to_dto(
        command: DiscoverCompaniesCommand,
    ) -> DiscoveryRequestDTO:

        return DiscoveryRequestDTO(

            industry=command.industry,

            location=command.location,

            max_results=command.max_results,
        )

    @staticmethod
    def dto_to_schema(
        dto: DiscoveryRequestDTO,
    ) -> DiscoveryRequest:

        return DiscoveryRequest(

            industry=dto.industry,

            location=dto.location,

            max_results=dto.max_results,
        )

    @staticmethod
    def results_to_response(
        results: list[
            DiscoveryResult
        ],
    ) -> DiscoveryResponseDTO:

        return DiscoveryResponseDTO(

            companies=[

                DiscoveryCompanyDTO(

                    company_name=item.company_name,

                    website=item.website,

                    industry=item.industry,

                    location=item.location,

                    source=item.source,

                    description=item.description,

                    employee_range=item.employee_range,

                    linkedin_url=item.linkedin_url,
                )

                for item in results

            ]
        )