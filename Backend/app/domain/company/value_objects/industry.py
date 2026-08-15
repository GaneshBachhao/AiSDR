from enum import StrEnum


class Industry(StrEnum):
    """
    Supported business industries.
    """

    MANUFACTURING = "Manufacturing"

    HEALTHCARE = "Healthcare"

    FINANCIAL_SERVICES = "Financial Services"

    RETAIL = "Retail"

    EDUCATION = "Education"

    INFORMATION_TECHNOLOGY = "Information Technology"

    LOGISTICS = "Logistics"

    CONSTRUCTION = "Construction"

    REAL_ESTATE = "Real Estate"

    HOSPITALITY = "Hospitality"

    AGRICULTURE = "Agriculture"

    GOVERNMENT = "Government"

    TELECOMMUNICATIONS = "Telecommunications"

    ENERGY = "Energy"

    OTHER = "Other"