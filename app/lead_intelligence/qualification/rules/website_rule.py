"""
Website Qualification Rule
"""

from app.company_intelligence.schemas.company_profile_schema import CompanyProfile
from app.lead_intelligence.qualification.rules.base_rule import (
    BaseQualificationRule,
)

from app.lead_intelligence.schemas.lead_candidate_schema import (
    LeadCandidate,
)

from app.lead_intelligence.qualification.schemas.icp_schema import (
    IdealCustomerProfile,
)

from app.lead_intelligence.qualification.schemas.rule_result_schema import (
    RuleResult,
)


class WebsiteRule(BaseQualificationRule):

    SCORE = 10

    def evaluate(
        self,
        company: CompanyProfile,
        icp: IdealCustomerProfile,
    ) -> RuleResult:

        if not icp.require_official_website:

            return RuleResult(
                passed=True,
                score=0,
                rule_name="Website",
                message="Website not required.",
            )

        if company.website:

            return RuleResult(
                passed=True,
                score=self.SCORE,
                rule_name="Website",
                message="Official website available.",
            )

        return RuleResult(
            passed=False,
            score=0,
            rule_name="Website",
            message="Website missing.",
            recommendation="Do not qualify automatically.",
        )