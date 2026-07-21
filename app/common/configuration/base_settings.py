"""
Base Settings

Shared base class for all AI BDOS configuration objects.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Dict


@dataclass(slots=True)
class BaseSettings:
    """
    Base class for strongly typed configuration.

    All configuration objects should inherit
    from this class.
    """

    # ------------------------------------------------------------------
    # Settings Metadata
    # ------------------------------------------------------------------

    name: str = "BaseSettings"

    version: str = "1.0.0"

    description: str = ""

    # ------------------------------------------------------------------
    # Extra Configuration
    # ------------------------------------------------------------------

    metadata: Dict[str, Any] = field(
        default_factory=dict,
    )

    @property
    def settings_type(self) -> str:
        """
        Returns the concrete settings type.
        """
        return self.__class__.__name__

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert settings to a dictionary.
        """
        return dict(self.__dict__)