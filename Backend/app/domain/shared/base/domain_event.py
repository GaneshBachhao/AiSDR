from abc import ABC
from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4


@dataclass(frozen=True)
class DomainEvent(ABC):
    """
    Base class for all domain events.

    Every concrete event is itself a ``@dataclass`` (e.g. ``CompanyCreated``),
    and dataclass field inheritance only works correctly when every class
    in the hierarchy is a dataclass -- a subclass's generated ``__init__``
    does not call an ordinary (non-dataclass) base class's ``__init__``.
    This used to be a plain class with a hand-written ``__init__``, which
    meant ``event_id``/``occurred_at`` were silently never set on any
    concrete event (accessing them raised ``AttributeError``). Never
    surfaced in practice because no concrete event is currently raised
    anywhere in the application -- found while writing the first real
    domain-event tests.
    """

    event_id: UUID = field(default_factory=uuid4, init=False)
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC), init=False)
