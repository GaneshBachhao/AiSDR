"""
Industry Qualification Rule
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


class IndustryRule(BaseQualificationRule):

    SCORE = 40

    def evaluate(
        self,
        company: CompanyProfile,
        icp: IdealCustomerProfile,
    ) -> RuleResult:

        if not icp.industries:

            return RuleResult(
                passed=True,
                score=0,
                rule_name="Industry",
                message="No industry restriction configured.",
            )

        candidate_industry = (
            company.industry or ""
        ).lower()

        valid_industries = [
            industry.lower()
            for industry in icp.industries
        ]

        if candidate_industry in valid_industries:

            return RuleResult(
                passed=True,
                score=self.SCORE,
                rule_name="Industry",
                message="Industry matched.",
            )

        return RuleResult(
            passed=False,
            score=0,
            rule_name="Industry",
            message="Industry does not match ICP.",
            recommendation="Skip this company.",
        )