from abc import ABC, abstractmethod
from typing import List

from app.core.domain.entities.UserRepository import User


class UserRepositoryDBPort(ABC):

    @abstractmethod
    async def get_all_Users(self) -> List[User]:  # type: ignore
        raise NotImplementedError

    @abstractmethod
    async def get_User_by_id(self, User_id: int) -> User:
        raise NotImplementedError

    @abstractmethod
    async def create_User(self, User: User) -> User:
        raise NotImplementedError

    @abstractmethod
    async def update_User(self, id: str, nombre: str, telefono: str) -> User:
        raise NotImplementedError
