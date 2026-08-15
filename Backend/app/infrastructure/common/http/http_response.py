from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class HttpResponse:
    """
    Generic HTTP response.
    """

    status_code: int

    body: Any

    headers: dict[str, str]

    @property
    def is_success(self) -> bool:
        return 200 <= self.status_code < 300