"""
Company Commands.

Architecture Freeze v5.0
Application command contracts for the Company aggregate.
"""
from __future__ import annotations

from app.application.common.commands.command import Command


class CreateCompanyCommand(Command):
    """Command to create a company."""

    name: str
    website: str | None = None
    industry: str | None = None
    company_size: str | None = None
    employee_count: int | None = None
    country: str | None = None
    state: str | None = None
    city: str | None = None


class UpdateCompanyCommand(Command):
    """Command to update a company."""

    company_id: str
    name: str | None = None
    website: str | None = None
    industry: str | None = None
    company_size: str | None = None
    employee_count: int | None = None
    country: str | None = None
    state: str | None = None
    city: str | None = None


class DeleteCompanyCommand(Command):
    """Command to delete a company."""

    company_id: str
