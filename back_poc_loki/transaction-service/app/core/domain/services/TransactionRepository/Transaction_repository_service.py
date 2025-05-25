import json
from pydantic.dataclasses import dataclass

from app.core.application.ports.database.Transaction_repository_db_port import (
    TransactionRepositoryDBPort
)
from app.core.application.ports.services.Transaction_repository_service_port import (
    TransactionRepositoryServicePort
)
from app.core.domain.entities.TransactionRepository.Transaction import Transaction


@dataclass(config=dict(arbitrary_types_allowed=True))
class TransactionRepositoryService(TransactionRepositoryServicePort):
    repo: TransactionRepositoryDBPort

    async def get_all_Transactions(self):
        print("Service implementation: OK")
        return await self.repo.get_all_Transactions()

    async def get_Transaction_by_id(self, Transaction_id: int):
        print("Service implementation: OK")
        return await self.repo.get_Transaction_by_id(Transaction_id)

    async def update_Transaction(self, id: str, nombre: str, telefono: str):
        print("Service implementation: OK")
        return await self.repo.update_Transaction(id, nombre, telefono)

    async def create_Transaction(self, Transaction: Transaction):
        print("Service implementation: OK")
        print(f"Request: {json.dumps(Transaction.__dict__, indent=2)}")
        return await self.repo.create_Transaction(Transaction)
