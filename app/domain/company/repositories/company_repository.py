from abc import ABC, abstractmethod

from app.domain.company.entities.company import Company


class CompanyRepository(ABC):
    """
    Repository interface for Company aggregate.
    """

    @abstractmethod
    def save(self, company: Company) -> Company:
        """Persist a company."""
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, company_id: str) -> Company | None:
        """Retrieve a company by its identifier."""
        raise NotImplementedError

    @abstractmethod
    def find_by_name(self, name: str) -> Company | None:
        """Retrieve a company by its name."""
        raise NotImplementedError

    @abstractmethod
    def exists(self, company_id: str) -> bool:
        """Check if a company exists."""
        raise NotImplementedError