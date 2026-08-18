from dataclasses import dataclass


@dataclass(frozen=True)
class ROI:
    """
    Represents the estimated return on investment.
    """

    percentage: float

    payback_period: str

    remarks: str | None = None

    def __post_init__(self) -> None:
        """
        Validate business invariants.
        """
        if self.percentage < 0:
            raise ValueError("ROI percentage cannot be negative.")

        if not self.payback_period.strip():
            raise ValueError("Payback period cannot be empty.")

        if self.remarks is not None and not self.remarks.strip():
            raise ValueError("Remarks cannot be empty.")
