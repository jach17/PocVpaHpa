from abc import abstractmethod, ABC

from app.core.domain.entities.TransactionAdapter.Transaction_dto import TransactionDto


class TransactionAdapterPort(ABC):
    @abstractmethod
    async def get_Transaction_by_id(self, Transaction_id: str) -> TransactionDto:
        raise NotImplementedError
