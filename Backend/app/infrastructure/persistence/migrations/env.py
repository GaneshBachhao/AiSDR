"""
Alembic migration environment.
"""

from __future__ import annotations

from logging.config import fileConfig

from alembic import context
from sqlalchemy import UUID, engine_from_config, pool

from app.infrastructure.persistence.database.base import Base

# ---------------------------------------------------------------------
# Import all ORM models so they are registered with Base.metadata
# ---------------------------------------------------------------------
from app.infrastructure.persistence.models.ai_request_model import (
    AIRequestModel,
)
from app.infrastructure.persistence.models.assessment_model import (
    AssessmentModel,
)
from app.infrastructure.persistence.models.company_model import (
    CompanyModel,
)
from app.infrastructure.persistence.models.contact_model import (
    ContactModel,
)
from app.infrastructure.persistence.models.discovery_model import (
    DiscoveryModel,
)
from app.infrastructure.persistence.models.lead_model import (
    LeadModel,
)
from app.infrastructure.persistence.models.qualification_model import (
    QualificationModel,
)
from app.infrastructure.persistence.models.recommendation_model import (
    RecommendationModel,
)
from app.infrastructure.persistence.models.user_model import (
    UserModel,
)

# ---------------------------------------------------------------------

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def compare_type(
    context,
    inspected_column,
    metadata_column,
    inspected_type,
    metadata_type,
):
    """
    Ignore SQLite UUID reflection differences.

    SQLite reflects UUID columns as NUMERIC,
    causing false-positive Alembic migrations.
    """

    if context.dialect.name == "sqlite":
        if isinstance(metadata_type, UUID):
            return False

    return None


def run_migrations_offline() -> None:
    """
    Run migrations in offline mode.
    """

    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=compare_type,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations in online mode.
    """

    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=compare_type,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
