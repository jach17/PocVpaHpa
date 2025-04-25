from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.core.application.ports.services.Transaction_repository_service_port import (
    TransactionRepositoryServicePort
)
from app.infrastructure.api.routers.dependencies import (
    get_Transaction_repository_service
)
from app.core.application.use_cases.repository.Transaction_repository_case import (
    create_Transaction_case,
    get_all_Transactions_case,
    update_Transaction_case
)
from app.infrastructure.api.schemas.Transaction_schema import TransactionCreate, TransactionResponse


router = APIRouter(
    prefix="/api/v1/repo/repository",
    tags=["Transactions"]
)


@router.post(
    path="/",
    response_model=TransactionResponse
)
async def create_Transaction(
    Transaction: TransactionCreate,
    repository: TransactionRepositoryServicePort = Depends(
        get_Transaction_repository_service
    )
):
    print("Router: OK")
    return await create_Transaction_case(
        Transaction_service_repository=repository,
        nombre=Transaction.nombre,
        telefono=Transaction.telefono
    )


@router.put(
    "/{Transaction_id}",
    response_model=TransactionResponse
)
async def update_Transaction(
    Transaction: TransactionCreate,
    Transaction_id: str,
    repository: TransactionRepositoryServicePort = Depends(
        get_Transaction_repository_service
    )
):
    print("Router: OK")
    updated = await update_Transaction_case(
        Transaction_service_repository=repository,
        id=Transaction_id,
        nombre=Transaction.nombre,
        telefono=Transaction.telefono
    )
    if updated:
        return updated
    return JSONResponse(status_code=404, content={"detail": "Transaction not found"})


@router.get("/")
async def list_Transactions(
    repository: TransactionRepositoryServicePort = Depends(
        get_Transaction_repository_service
    )
):
    print("Router: OK")
    return await get_all_Transactions_case(Transaction_service_repository=repository)
