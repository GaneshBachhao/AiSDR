from enum import StrEnum


class Currency(StrEnum):
    """
    Supported currencies for financial estimates.
    """

    USD = "USD"

    EUR = "EUR"

    INR = "INR"