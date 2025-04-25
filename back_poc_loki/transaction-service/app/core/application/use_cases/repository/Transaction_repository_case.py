import json
from app.core.application.ports.services.Transaction_repository_service_port import (
    TransactionRepositoryServicePort
)
from app.core.domain.entities.TransactionRepository.Transaction import Transaction


async def get_all_Transactions_case(
    Transaction_service_repository: TransactionRepositoryServicePort
):
    print("Use cases: OK")
    return await Transaction_service_repository.get_all_Transactions()


async def get_Transaction_case(
    Transaction_service_repository: TransactionRepositoryServicePort,
    Transaction_id: int
):
    print("Use cases: OK")
    return await Transaction_service_repository.get_Transaction_by_id(Transaction_id)


async def update_Transaction_case(
    Transaction_service_repository: TransactionRepositoryServicePort,
    id: str,
    nombre: str,
    telefono: str
):
    print("Use cases: OK")
    return await Transaction_service_repository.update_Transaction(id, nombre, telefono)


async def create_Transaction_case(
    Transaction_service_repository: TransactionRepositoryServicePort,
    nombre: str,
    telefono: str
):
    obj = Transaction(id=0, nombre=nombre, telefono=telefono)
    print("Use case: OK")
    print(f"Request: {json.dumps(obj.__dict__, indent=2)}")
    return await Transaction_service_repository.create_Transaction(obj)
