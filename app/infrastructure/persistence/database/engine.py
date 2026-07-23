"""
Database engine configuration.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
)


def create_engine(
    connection_string: str,
    *,
    echo: bool = False,
    pool_pre_ping: bool = True,
) -> AsyncEngine:
    """
    Create a SQLAlchemy asynchronous engine.

    Args:
        connection_string:
            Database connection string.

        echo:
            Enable SQL statement logging.

        pool_pre_ping:
            Validate pooled connections before use.

    Returns:
        Configured AsyncEngine instance.
    """

    return create_async_engine(
        connection_string,
        echo=echo,
        future=True,
        pool_pre_ping=pool_pre_ping,
    )