# app/application/common/interfaces/event_publisher.py

"""
Domain event publishing application port.

Infrastructure implementations may use message brokers,
queues, or in-process dispatchers.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.shared.base.domain_event import DomainEvent


class EventPublisher(ABC):
    """
    Contract for publishing domain events.
    """

    @abstractmethod
    async def publish(
        self,
        event: DomainEvent,
    ) -> None:
        """
        Publish a domain event.
        """
        raise NotImplementedError

    @abstractmethod
    async def publish_many(
        self,
        events: list[DomainEvent],
    ) -> None:
        """
        Publish multiple domain events.
        """
        raise NotImplementedError
