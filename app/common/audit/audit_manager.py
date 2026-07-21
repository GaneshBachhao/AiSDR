"""
Audit Manager

Central audit manager for AI BDOS.
"""

from typing import List

from common.audit.audit_configuration import (
    AuditConfiguration,
)
from common.audit.audit_event import (
    AuditEvent,
)


class AuditManager:
    """
    Central audit manager.

    Responsible for recording and retrieving
    audit events.
    """

    _configuration = AuditConfiguration()

    _events: List[AuditEvent] = []

    @classmethod
    def configure(
        cls,
        configuration: AuditConfiguration,
    ) -> None:
        """
        Configure the audit framework.
        """
        cls._configuration = configuration

    @classmethod
    def record(
        cls,
        event: AuditEvent,
    ) -> None:
        """
        Record an audit event.
        """

        if not cls._configuration.enabled:
            return

        if cls._configuration.retain_events:
            cls._events.append(event)

    @classmethod
    def events(
        cls,
    ) -> List[AuditEvent]:
        """
        Return recorded audit events.
        """

        return list(cls._events)

    @classmethod
    def clear(
        cls,
    ) -> None:
        """
        Remove all audit events.

        Intended for testing.
        """

        cls._events.clear()