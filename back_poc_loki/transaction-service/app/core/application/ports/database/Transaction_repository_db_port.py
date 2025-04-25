from abc import ABC, abstractmethod
from typing import List

from app.core.domain.entities.TransactionRepository import Transaction


class TransactionRepositoryDBPort(ABC):

    @abstractmethod
    async def get_all_Transactions(self) -> List[Transaction]:  # type: ignore
        raise NotImplementedError

    @abstractmethod
    async def get_Transaction_by_id(self, Transaction_id: int) -> Transaction:
        raise NotImplementedError

    @abstractmethod
    async def create_Transaction(self, Transaction: Transaction) -> Transaction:
        raise NotImplementedError

    @abstractmethod
    async def update_Transaction(self, id: str, nombre: str, telefono: str) -> Transaction:
        raise NotImplementedError
