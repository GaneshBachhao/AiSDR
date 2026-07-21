"""
Audit Configuration

Shared audit configuration for AI BDOS.
"""

from dataclasses import asdict
from dataclasses import dataclass
from typing import Any
from typing import Dict


@dataclass(slots=True)
class AuditConfiguration:
    """
    Audit framework configuration.
    """

    # ------------------------------------------------------------------
    # Configuration Metadata
    # ------------------------------------------------------------------

    name: str = "AuditConfiguration"

    version: str = "1.0.0"

    description: str = ""

    # ------------------------------------------------------------------
    # Audit Settings
    # ------------------------------------------------------------------

    enabled: bool = True

    include_timestamp: bool = True

    include_user: bool = True

    include_module: bool = True

    retain_events: bool = True

    @property
    def configuration_type(self) -> str:
        """
        Returns the configuration type.
        """
        return self.__class__.__name__

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary.
        """
        return asdict(self)