from dataclasses import dataclass

from app.domain.shared.enums import Currency


@dataclass(frozen=True)
class CostEstimate:
    """
    Represents the estimated implementation cost.
    """

    amount: float

    currency: Currency = Currency.USD

    remarks: str | None = None

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError("Cost estimate cannot be negative.")

        if self.remarks is not None and not self.remarks.strip():
            raise ValueError("Remarks cannot be empty.")
