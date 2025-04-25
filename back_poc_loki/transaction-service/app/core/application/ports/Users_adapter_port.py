from abc import abstractmethod, ABC

from app.core.domain.entities.UsersAdapter.Users_dto import UsersDto


class UsersAdapterPort(ABC):
    @abstractmethod
    async def get_Users_by_id(self, Users_id: str) -> UsersDto:
        raise NotImplementedError
