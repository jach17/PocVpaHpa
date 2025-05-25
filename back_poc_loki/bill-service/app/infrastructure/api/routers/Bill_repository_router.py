from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.core.application.ports.services.Bill_repository_service_port import (
    BillRepositoryServicePort
)
from app.infrastructure.api.routers.dependencies import (
    get_Bill_repository_service
)
from app.core.application.use_cases.repository.Bill_repository_case import (
    create_Bill_case,
    get_all_Bills_case,
    update_Bill_case
)
from app.infrastructure.api.schemas.Bill_schema import BillCreate, BillResponse


router = APIRouter(
    prefix="/api/v1/repo/repository",
    tags=["Bills"]
)


@router.post(
    path="/",
    response_model=BillResponse
)
async def create_Bill(
    Bill: BillCreate,
    repository: BillRepositoryServicePort = Depends(
        get_Bill_repository_service
    )
):
    print("Router: OK")
    return await create_Bill_case(
        Bill_service_repository=repository,
        nombre=Bill.nombre,
        telefono=Bill.telefono
    )


@router.put(
    "/{Bill_id}",
    response_model=BillResponse
)
async def update_Bill(
    Bill: BillCreate,
    Bill_id: str,
    repository: BillRepositoryServicePort = Depends(
        get_Bill_repository_service
    )
):
    print("Router: OK")
    updated = await update_Bill_case(
        Bill_service_repository=repository,
        id=Bill_id,
        nombre=Bill.nombre,
        telefono=Bill.telefono
    )
    if updated:
        return updated
    return JSONResponse(status_code=404, content={"detail": "Bill not found"})


@router.get("/")
async def list_Bills(
    repository: BillRepositoryServicePort = Depends(
        get_Bill_repository_service
    )
):
    print("Router: OK")
    return await get_all_Bills_case(Bill_service_repository=repository)
