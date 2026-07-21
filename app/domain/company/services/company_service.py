from app.domain.company.entities.company import Company


class CompanyService:
    """
    Domain service for Company-related business operations.
    """

    @staticmethod
    def activate(company: Company) -> None:
        """
        Activate a company.
        """
        company.activate()

    @staticmethod
    def deactivate(company: Company) -> None:
        """
        Deactivate a company.
        """
        company.deactivate()