from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class ValidationResult:
    """
    Represents validation outcome.
    """

    errors: Dict[str, List[str]] = field(default_factory=dict)

    @property
    def is_valid(self) -> bool:
        return not self.errors

    def add_error(self, field: str, message: str) -> None:
        if field not in self.errors:
            self.errors[field] = []

        self.errors[field].append(message)

    def has_error(self, field: str) -> bool:
        return field in self.errors

    def get_errors(self, field: str) -> List[str]:
        return self.errors.get(field, [])