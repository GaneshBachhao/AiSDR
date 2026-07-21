"""
Rule Registry

Provides the ordered list of qualification
rules used by the qualification engine.
"""

from app.lead_intelligence.qualification.rules import keyword_rule
from app.lead_intelligence.qualification.rules.base_rule import (
    BaseQualificationRule,
)

from app.lead_intelligence.qualification.rules.employee_rule import EmployeeRule
from app.lead_intelligence.qualification.rules.industry_rule import IndustryRule
from app.lead_intelligence.qualification.rules.location_rule import LocationRule
from app.lead_intelligence.qualification.rules.website_rule import WebsiteRule
from app.lead_intelligence.qualification.rules.keyword_rule import KeywordRule 

class RuleRegistry:
    """
    Registry of qualification rules.
    """

    @staticmethod
    def get_rules() -> list[BaseQualificationRule]:
        """
        Returns all enabled qualification rules
        in execution order.
        """

        return [

            IndustryRule(),
            LocationRule(),
            WebsiteRule(),
            KeywordRule(), 
            EmployeeRule(),

        ]