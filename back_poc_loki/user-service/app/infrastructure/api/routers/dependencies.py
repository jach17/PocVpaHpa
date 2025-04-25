from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.application.ports.database.User_repository_db_port import (
    UserRepositoryDBPort
)
from app.core.application.use_cases.repository.User_repository_case import (
    UserRepositoryServicePort
)
from app.core.domain.services.UserRepository.User_repository_service import (
    UserRepositoryService
)
from app.infrastructure.database.repositories.User_repository import (
    UserRepository
    )
from app.infrastructure.database.session import get_db

SessionDep = Annotated[AsyncSession, Depends(get_db)]


def get_User_repository(
    session: AsyncSession = Depends(get_db)
) -> UserRepository:
    return UserRepository(session=session)


def get_User_repository_service(
    repo: UserRepositoryDBPort = Depends(get_User_repository)
) -> (
    UserRepositoryServicePort
):
    return UserRepositoryService(
        repo=repo
    )
