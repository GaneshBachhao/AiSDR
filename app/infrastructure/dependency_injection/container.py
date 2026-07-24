"""
Infrastructure dependency container.
"""

from __future__ import annotations

from app.infrastructure.configuration.database_settings import DatabaseSettings
from app.infrastructure.dependency_injection.database import (
    DatabaseProvider,
)


class Container:
    """
    Root infrastructure container.
    """

    def __init__(
        self,
        settings: DatabaseSettings,
    ) -> None:

        self.database = DatabaseProvider(settings)