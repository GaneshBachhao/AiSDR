"""
Report Domain Module.

Responsible for report composition,
review, versioning and publication.
"""

from .aggregate import Report

from .entities import (
    ReportSection,
    ReportVersion,
)

from .value_objects import (
    ReportId,
    ReportName,
    SectionId,
    VersionId,
    VersionNumber,
)

from .enums import (
    ReportStatus,
    SectionStatus,
)

__all__ = [
    "Report",

    "ReportSection",
    "ReportVersion",

    "ReportId",
    "ReportName",
    "SectionId",
    "VersionId",
    "VersionNumber",

    "ReportStatus",
    "SectionStatus",
]