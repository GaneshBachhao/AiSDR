"""
Logging Configuration

Shared logging configuration for AI BDOS.
"""

from dataclasses import asdict
from dataclasses import dataclass
from typing import Any
from typing import Dict


@dataclass(slots=True)
class LoggingConfiguration:
    """
    Logging configuration.

    Defines the standard logging behavior
    for the application.
    """

    # ------------------------------------------------------------------
    # Configuration Metadata
    # ------------------------------------------------------------------

    name: str = "LoggingConfiguration"

    version: str = "1.0.0"

    description: str = ""

    # ------------------------------------------------------------------
    # Logging Settings
    # ------------------------------------------------------------------

    level: str = "INFO"

    format: str = (
        "%(asctime)s | "
        "%(levelname)-8s | "
        "%(name)s | "
        "%(message)s"
    )

    date_format: str = "%Y-%m-%d %H:%M:%S"

    enable_console: bool = True

    enable_file: bool = False

    file_name: str = "aibdos.log"

    @property
    def configuration_type(self) -> str:
        """
        Returns the concrete configuration type.
        """
        return self.__class__.__name__

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the configuration to a dictionary.
        """
        return asdict(self)