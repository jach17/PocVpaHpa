import json
from pydantic.dataclasses import dataclass

from app.core.application.ports.database.Bill_repository_db_port import (
    BillRepositoryDBPort
)
from app.core.application.ports.services.Bill_repository_service_port import (
    BillRepositoryServicePort
)
from app.core.domain.entities.BillRepository.Bill import Bill


@dataclass(config=dict(arbitrary_types_allowed=True))
class BillRepositoryService(BillRepositoryServicePort):
    repo: BillRepositoryDBPort

    async def get_all_Bills(self):
        print("Service implementation: OK")
        return await self.repo.get_all_Bills()

    async def get_Bill_by_id(self, Bill_id: int):
        print("Service implementation: OK")
        return await self.repo.get_Bill_by_id(Bill_id)

    async def update_Bill(self, id: str, nombre: str, telefono: str):
        print("Service implementation: OK")
        return await self.repo.update_Bill(id, nombre, telefono)

    async def create_Bill(self, Bill: Bill):
        print("Service implementation: OK")
        print(f"Request: {json.dumps(Bill.__dict__, indent=2)}")
        return await self.repo.create_Bill(Bill)
