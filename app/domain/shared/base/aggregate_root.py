# app/domain/shared/base/aggregate_root.py

from __future__ import annotations

from abc import ABC
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Generic, TypeVar

from app.domain.shared.base.domain_event import DomainEvent
from app.domain.shared.base.entity import Entity
from app.domain.shared.identifiers import Identifier


TId = TypeVar("TId", bound=Identifier)


@dataclass(eq=False)
class AggregateRoot(
    Entity[TId],
    ABC,
    Generic[TId],
):
    """
    Base class for all aggregate roots.

    Aggregate roots extend Entity with:

    - Audit timestamps
    - Domain event collection
    """

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
        kw_only=True,
    )

    updated_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
        kw_only=True,
    )

    _domain_events: list[DomainEvent] = field(
        default_factory=list,
        init=False,
        repr=False,
    )

    @property
    def domain_events(self) -> tuple[DomainEvent, ...]:
        """
        Return all pending domain events.
        """
        return tuple(self._domain_events)

    def add_domain_event(
        self,
        event: DomainEvent,
    ) -> None:
        """
        Register a domain event.
        """
        self._domain_events.append(event)

    def remove_domain_event(
        self,
        event: DomainEvent,
    ) -> None:
        """
        Remove a specific domain event.
        """
        if event in self._domain_events:
            self._domain_events.remove(event)

    def clear_domain_events(self) -> None:
        """
        Remove all pending domain events.
        """
        self._domain_events.clear()

    def touch(self) -> None:
        """
        Update the modification timestamp.
        """
        self.updated_at = datetime.now(UTC)