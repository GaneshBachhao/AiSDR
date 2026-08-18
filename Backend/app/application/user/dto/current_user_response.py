"""
Current user response DTO.
"""

from __future__ import annotations

from pydantic import BaseModel


class CurrentUserResponseDTO(BaseModel):
    """Response DTO for the authenticated user's own profile."""

    id: str
    email: str
    is_active: bool
