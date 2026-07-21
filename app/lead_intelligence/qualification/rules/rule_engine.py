"""
Qualification Rule Engine

Executes all qualification rules and
produces a QualificationResult.
"""

from app.company_intelligence.schemas.company_profile_schema import CompanyProfile
from app.lead_intelligence.schemas.lead_candidate_schema import (
    LeadCandidate,
)

from app.lead_intelligence.qualification.schemas.icp_schema import (
    IdealCustomerProfile,
)

from app.lead_intelligence.qualification.schemas.qualification_result_schema import (
    QualificationResult,
)

from app.lead_intelligence.qualification.rules.rule_registry import (
    RuleRegistry,
)


class QualificationRuleEngine:
    """
    Executes all registered qualification rules.
    """

    
    def evaluate(
        self,
        company: CompanyProfile,
        icp: IdealCustomerProfile,
    ) -> QualificationResult:

        total_score = 0

        matched_rules = []

        failed_rules = []

        recommendations = []

        for rule in RuleRegistry.get_rules():

            result = rule.evaluate(
                company,
                icp,
            )

            total_score += result.score

            if result.passed:

                matched_rules.append(
                    result.message,
                )

            else:

                failed_rules.append(
                    result.message,
                )

                if result.recommendation:

                    recommendations.append(
                        result.recommendation,
                    )

        return QualificationResult(

            qualified = (
                total_score >= icp.passing_score
            ),

            score=total_score,

            matched_rules=matched_rules,

            failed_rules=failed_rules,

            recommendations=recommendations,
        )