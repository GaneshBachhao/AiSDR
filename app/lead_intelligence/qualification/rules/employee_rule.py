"""
Employee Qualification Rule
"""

from app.lead_intelligence.qualification.rules.base_rule import BaseQualificationRule
from app.lead_intelligence.schemas.lead_candidate_schema import LeadCandidate
from app.lead_intelligence.qualification.schemas.icp_schema import IdealCustomerProfile
from app.lead_intelligence.qualification.schemas.rule_result_schema import RuleResult


class EmployeeRule(BaseQualificationRule):

    SCORE = 20

    def evaluate(self, company, icp):

        if company.employee_count is None:

            return RuleResult(
                passed=True,
                score=0,
                rule_name="Employees",
                message="Employee count unavailable.",
            )

        if (
            icp.employee_min is not None
            and company.employee_count < icp.employee_min
        ):
            return RuleResult(
                passed=False,
                score=0,
                rule_name="Employees",
                message="Company is smaller than ICP.",
            )

        if (
            icp.employee_max is not None
            and company.employee_count > icp.employee_max
        ):
            return RuleResult(
                passed=False,
                score=0,
                rule_name="Employees",
                message="Company is larger than ICP.",
            )

        return RuleResult(
            passed=True,
            score=self.SCORE,
            rule_name="Employees",
            message="Employee size matched.",
        )