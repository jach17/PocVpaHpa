from abc import ABC, abstractmethod
from typing import List

from app.core.domain.entities.BillRepository import Bill


class BillRepositoryDBPort(ABC):

    @abstractmethod
    async def get_all_Bills(self) -> List[Bill]:  # type: ignore
        raise NotImplementedError

    @abstractmethod
    async def get_Bill_by_id(self, Bill_id: int) -> Bill:
        raise NotImplementedError

    @abstractmethod
    async def create_Bill(self, Bill: Bill) -> Bill:
        raise NotImplementedError

    @abstractmethod
    async def update_Bill(self, id: str, nombre: str, telefono: str) -> Bill:
        raise NotImplementedError
