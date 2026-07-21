"""
Audit Event

Represents a single auditable platform event.
"""

from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from typing import Any
from typing import Dict


@dataclass(slots=True)
class AuditEvent:
    """
    Represents an auditable event within AI BDOS.
    """

    # ------------------------------------------------------------------
    # Event Identity
    # ------------------------------------------------------------------

    event_type: str

    module: str

    # ------------------------------------------------------------------
    # Event Context
    # ------------------------------------------------------------------

    actor: str = "system"

    success: bool = True

    message: str = ""

    # ------------------------------------------------------------------
    # Event Metadata
    # ------------------------------------------------------------------

    timestamp: datetime = field(
        default_factory=datetime.utcnow,
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict,
    )

    @property
    def event_name(self) -> str:
        """
        Returns the event type.
        """
        return self.event_type

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the audit event to a dictionary.
        """
        return asdict(self)