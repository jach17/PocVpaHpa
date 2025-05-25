import json
from app.core.application.ports.services.Bill_repository_service_port import (
    BillRepositoryServicePort
)
from app.core.domain.entities.BillRepository.Bill import Bill


async def get_all_Bills_case(
    Bill_service_repository: BillRepositoryServicePort
):
    print("Use cases: OK")
    return await Bill_service_repository.get_all_Bills()


async def get_Bill_case(
    Bill_service_repository: BillRepositoryServicePort,
    Bill_id: int
):
    print("Use cases: OK")
    return await Bill_service_repository.get_Bill_by_id(Bill_id)


async def update_Bill_case(
    Bill_service_repository: BillRepositoryServicePort,
    id: str,
    nombre: str,
    telefono: str
):
    print("Use cases: OK")
    return await Bill_service_repository.update_Bill(id, nombre, telefono)


async def create_Bill_case(
    Bill_service_repository: BillRepositoryServicePort,
    nombre: str,
    telefono: str
):
    obj = Bill(id=0, nombre=nombre, telefono=telefono)
    print("Use case: OK")
    print(f"Request: {json.dumps(obj.__dict__, indent=2)}")
    return await Bill_service_repository.create_Bill(obj)
