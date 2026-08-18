"""
Base persistence model.

Defines the abstract base class inherited by every ORM model.
"""

from __future__ import annotations

from app.infrastructure.persistence.database.base import Base
from app.infrastructure.persistence.models.audit_mixin import (
    AuditMixin,
)
from app.infrastructure.persistence.models.entity_mixin import (
    EntityMixin,
)
from app.infrastructure.persistence.models.soft_delete_mixin import (
    SoftDeleteMixin,
)
from app.infrastructure.persistence.models.timestamp_mixin import (
    TimestampMixin,
)


class BaseModel(
    Base,
    EntityMixin,
    TimestampMixin,
    AuditMixin,
    SoftDeleteMixin,
):
    """
    Abstract base class for all persistence models.
    """

    __abstract__ = True
