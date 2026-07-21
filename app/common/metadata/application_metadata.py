"""
Application Metadata

Represents application-level metadata.
"""

from dataclasses import asdict
from dataclasses import dataclass
from typing import Any
from typing import Dict


@dataclass(slots=True)
class ApplicationMetadata:
    """
    Platform application metadata.
    """

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    application_name: str = "AI BDOS"

    version: str = "1.0.0"

    description: str = ""

    # ------------------------------------------------------------------
    # Build Information
    # ------------------------------------------------------------------

    environment: str = "development"

    build_number: str = ""

    build_date: str = ""

    git_commit: str = ""

    # ------------------------------------------------------------------
    # Ownership
    # ------------------------------------------------------------------

    author: str = ""

    company: str = ""

    license: str = ""

    @property
    def metadata_type(self) -> str:
        """
        Returns the metadata type.
        """
        return self.__class__.__name__

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert metadata to a dictionary.
        """
        return asdict(self)