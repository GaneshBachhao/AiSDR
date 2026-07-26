"""
Persistence dependencies.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends

from app.application.common.interfaces.unit_of_work import (
    UnitOfWork,
)
from app.infrastructure.dependency_injection.provider import (
    get_unit_of_work,
)


def get_unit_of_work_dependency() -> UnitOfWork:
    """
    Resolve the application Unit of Work.
    """

    return get_unit_of_work()


UnitOfWorkDependency = Annotated[
    UnitOfWork,
    Depends(get_unit_of_work_dependency),
]