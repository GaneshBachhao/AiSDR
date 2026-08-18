"""
SQLAlchemy declarative base.

This module defines the root declarative base used by every ORM
model within the persistence layer. It also configures metadata
naming conventions and automatic table name generation.
"""

from __future__ import annotations

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, declared_attr

NAMING_CONVENTION: dict[str, str] = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": ("fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s"),
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    """
    Root SQLAlchemy declarative base.

    All ORM models inherit, directly or indirectly,
    from this class.
    """

    metadata = MetaData(
        naming_convention=NAMING_CONVENTION,
    )

    @declared_attr.directive
    @classmethod
    def __tablename__(cls) -> str:
        """
        Automatically generate snake_case table names
        from model class names.
        """

        characters: list[str] = []

        for index, character in enumerate(
            cls.__name__,
        ):
            if character.isupper() and index > 0:
                characters.append("_")

            characters.append(
                character.lower(),
            )

        return "".join(characters)
