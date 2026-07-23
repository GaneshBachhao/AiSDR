from typing import Annotated

from fastapi import Depends

from app.infrastructure.dependency_injection.provider import get_unit_of_work
from app.infrastructure.persistence.unit_of_work import UnitOfWork


def get_unit_of_work_dependency() -> UnitOfWork:
    """
    Resolve the Unit of Work.
    """
    return get_unit_of_work()


UnitOfWorkDependency = Annotated[
    UnitOfWork,
    Depends(get_unit_of_work_dependency),
]