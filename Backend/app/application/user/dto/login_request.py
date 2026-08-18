"""
Login request DTO.
"""

from __future__ import annotations

from pydantic import BaseModel


class LoginRequestDTO(BaseModel):
    """Request DTO to log in."""

    email: str
    password: str
