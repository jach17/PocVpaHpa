from abc import abstractmethod, ABC

from app.core.domain.entities.EmptyAdapter.Empty_dto import EmptyDto


class EmptyAdapterPort(ABC):
    @abstractmethod
    async def get_Empty_by_id(self, Empty_id: str) -> EmptyDto:
        raise NotImplementedError
