from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.application.ports.database.Transaction_repository_db_port import (
    TransactionRepositoryDBPort
)
from app.core.application.use_cases.repository.Transaction_repository_case import (
    TransactionRepositoryServicePort
)
from app.core.domain.services.TransactionRepository.Transaction_repository_service import (
    TransactionRepositoryService
)
from app.infrastructure.database.repositories.Transaction_repository import (
    TransactionRepository
    )
from app.infrastructure.database.session import get_db

SessionDep = Annotated[AsyncSession, Depends(get_db)]


def get_Transaction_repository(
    session: AsyncSession = Depends(get_db)
) -> TransactionRepository:
    return TransactionRepository(session=session)


def get_Transaction_repository_service(
    repo: TransactionRepositoryDBPort = Depends(get_Transaction_repository)
) -> (
    TransactionRepositoryServicePort
):
    return TransactionRepositoryService(
        repo=repo
    )
