from enum import Enum


class BudgetIndicator(str, Enum):
    UNKNOWN = "UNKNOWN"
    NO_BUDGET = "NO_BUDGET"
    LIMITED = "LIMITED"
    APPROVED = "APPROVED"
    ENTERPRISE = "ENTERPRISE"