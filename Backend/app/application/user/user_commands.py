"""
User commands.

Application command contracts for the User aggregate.
"""

from __future__ import annotations

from app.application.common.commands.command import Command


class LoginCommand(Command):
    """Command to log in with an email and password."""

    email: str
    password: str
