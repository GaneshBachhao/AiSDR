"""
User identifier.
"""

from __future__ import annotations

from app.domain.shared.identifiers.identifier import Identifier


class UserId(Identifier):
    """Strongly typed User UUID identifier."""
