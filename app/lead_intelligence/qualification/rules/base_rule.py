"""
Base Qualification Rule
"""

from abc import ABC, abstractmethod

from app.company_intelligence.schemas.company_profile_schema import CompanyProfile
from app.lead_intelligence.schemas.lead_candidate_schema import (
    LeadCandidate,
)

from app.lead_intelligence.qualification.schemas.icp_schema import (
    IdealCustomerProfile,
)

from app.lead_intelligence.qualification.schemas.rule_result_schema import (
    RuleResult,
)


class BaseQualificationRule(ABC):
    """
    Base class for every qualification rule.
    """

    @abstractmethod
    def evaluate(
        self,
        company: CompanyProfile,
        icp: IdealCustomerProfile,
    ) -> RuleResult:
        """
        Evaluate a single qualification rule.
        """
        raise NotImplementedError