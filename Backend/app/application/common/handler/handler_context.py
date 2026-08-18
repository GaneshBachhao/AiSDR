from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4


@dataclass(slots=True)
class HandlerContext:
    """
    Context shared across the application layer.

    Carries execution-scoped information that should
    not be embedded inside commands.
    """

    db: Any | None = None

    correlation_id: str = field(
        default_factory=lambda: str(uuid4()),
    )

    request_id: str = field(
        default_factory=lambda: str(uuid4()),
    )

    user_id: str | None = None

    tenant_id: str | None = None

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )

    def add_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Store execution metadata.
        """

        self.metadata[key] = value

    def get_metadata(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Retrieve execution metadata.
        """

        return self.metadata.get(
            key,
            default,
        )

    @property
    def has_user(self) -> bool:
        """
        Whether a user identity exists.
        """

        return self.user_id is not None

    def to_dict(
        self,
    ) -> dict[str, Any]:
        """
        Serialize the execution context.
        """

        return {
            "correlation_id": self.correlation_id,
            "request_id": self.request_id,
            "user_id": self.user_id,
            "tenant_id": self.tenant_id,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
        }
