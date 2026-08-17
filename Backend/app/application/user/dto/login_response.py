"""
Login response DTO.
"""
from __future__ import annotations

from pydantic import BaseModel

from app.application.user.dto.current_user_response import CurrentUserResponseDTO


class LoginResponseDTO(BaseModel):
    """Response DTO returned after a successful login."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: CurrentUserResponseDTO
