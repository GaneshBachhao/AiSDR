"""
Qualification Service
"""

from app.company_intelligence.schemas.company_profile_schema import CompanyProfile
from app.lead_intelligence.schemas.lead_candidate_schema import (
    LeadCandidate,
)

from app.lead_intelligence.qualification.schemas.icp_schema import (
    IdealCustomerProfile,
)

from app.lead_intelligence.qualification.rules.rule_engine import (
    QualificationRuleEngine,
)

from app.lead_intelligence.qualification.schemas.qualification_result_schema import (
    QualificationResult,
)


class QualificationService:
    """
    Runs qualification against an ICP.
    """

    def __init__(self):

        self.engine = QualificationRuleEngine()

    def qualify(
        self,
        company: CompanyProfile,
        icp: IdealCustomerProfile,
    ) -> QualificationResult:

        return self.engine.evaluate(
            company,
            icp,
        )