"""
Keyword Qualification Rule
"""

from app.lead_intelligence.qualification.rules.base_rule import BaseQualificationRule
from app.lead_intelligence.schemas.lead_candidate_schema import LeadCandidate
from app.lead_intelligence.qualification.schemas.icp_schema import IdealCustomerProfile
from app.lead_intelligence.qualification.schemas.rule_result_schema import RuleResult


class KeywordRule(BaseQualificationRule):

    SCORE = 10

    def evaluate(self, company, icp):

        if not icp.include_keywords:

            return RuleResult(
                passed=True,
                score=0,
                rule_name="Keywords",
                message="No keyword restriction configured.",
            )

        searchable = " ".join([
            company.company_name or "",
            company.industry or "",
        ]).lower()

        for keyword in icp.include_keywords:

            if keyword.lower() in searchable:

                return RuleResult(
                    passed=True,
                    score=self.SCORE,
                    rule_name="Keywords",
                    message=f"Matched keyword '{keyword}'.",
                )

        return RuleResult(
            passed=False,
            score=0,
            rule_name="Keywords",
            message="No ICP keywords matched.",
        )