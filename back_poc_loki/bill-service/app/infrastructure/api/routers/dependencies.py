from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.application.ports.database.Bill_repository_db_port import (
    BillRepositoryDBPort
)
from app.core.application.use_cases.repository.Bill_repository_case import (
    BillRepositoryServicePort
)
from app.core.domain.services.BillRepository.Bill_repository_service import (
    BillRepositoryService
)
from app.infrastructure.database.repositories.Bill_repository import (
    BillRepository
    )
from app.infrastructure.database.session import get_db

SessionDep = Annotated[AsyncSession, Depends(get_db)]


def get_Bill_repository(
    session: AsyncSession = Depends(get_db)
) -> BillRepository:
    return BillRepository(session=session)


def get_Bill_repository_service(
    repo: BillRepositoryDBPort = Depends(get_Bill_repository)
) -> (
    BillRepositoryServicePort
):
    return BillRepositoryService(
        repo=repo
    )
