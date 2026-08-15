from dataclasses import dataclass


@dataclass(frozen=True)
class TimeoutPolicy:
    """
    HTTP timeout configuration.
    """

    connect_timeout: float = 10.0

    read_timeout: float = 60.0

    write_timeout: float = 60.0

    pool_timeout: float = 10.0

    def __post_init__(self) -> None:

        for value in (
            self.connect_timeout,
            self.read_timeout,
            self.write_timeout,
            self.pool_timeout,
        ):
            if value <= 0:
                raise ValueError(
                    "Timeout values must be positive."
                )