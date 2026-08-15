from enum import StrEnum


class FindingType(StrEnum):
    """
    Classification of assessment findings.
    """

    GAP = "Gap"

    RISK = "Risk"

    OPPORTUNITY = "Opportunity"

    STRENGTH = "Strength"

    OBSERVATION = "Observation"