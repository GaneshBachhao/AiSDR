from dataclasses import dataclass


@dataclass(frozen=True)
class RetryPolicy:
    """
    HTTP retry configuration.
    """

    max_attempts: int = 3

    backoff_seconds: float = 1.0

    exponential_backoff: bool = True

    def __post_init__(self) -> None:

        if self.max_attempts <= 0:
            raise ValueError("max_attempts must be greater than zero.")

        if self.backoff_seconds <= 0:
            raise ValueError("backoff_seconds must be greater than zero.")
