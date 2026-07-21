"""
Location Qualification Rule
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


class LocationRule(BaseQualificationRule):

    SCORE = 20

    def evaluate(
        self,
        company: CompanyProfile,
        icp: IdealCustomerProfile,
    ) -> RuleResult:

        if not icp.locations:

            return RuleResult(
                passed=True,
                score=0,
                rule_name="Location",
                message="No location restriction configured.",
            )

        candidate_locations = [
            (company.city or "").lower(),
            (company.state or "").lower(),
            (company.country or "").lower(),
        ]

        valid_locations = [
            location.lower()
            for location in icp.locations
        ]

        for location in candidate_locations:

            if location and location in valid_locations:

                return RuleResult(
                    passed=True,
                    score=self.SCORE,
                    rule_name="Location",
                    message="Location matched.",
                )

        return RuleResult(
            passed=False,
            score=0,
            rule_name="Location",
            message="Location does not match ICP.",
            recommendation="Skip this company.",
        )