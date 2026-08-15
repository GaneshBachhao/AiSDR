from abc import ABC
from datetime import UTC, datetime
from uuid import UUID, uuid4


class DomainEvent(ABC):
    """
    Base class for all domain events.
    """

    def __init__(self):
        self._event_id = uuid4()
        self._occurred_at = datetime.now(UTC)

    @property
    def event_id(self) -> UUID:
        return self._event_id

    @property
    def occurred_at(self) -> datetime:
        return self._occurred_at