from fastapi import APIRouter, HTTPException

from app.core.application.factories.builder_Transaction_service import (
    builder_Transaction_adapter_use_case
)
from app.infrastructure.api.schemas.exceptions import BusinessError
from app.infrastructure.api.schemas.Bill_schema import TransactionResponseService

router = APIRouter(
    prefix="/api/v1/bill",
    tags=["Transaction"]
)


@router.get(
    path="",
    response_model=TransactionResponseService
)
async def get_Transaction_by_id(
        Transaction_id: str
):
    try:
        use_case = builder_Transaction_adapter_use_case()
        return await use_case.get_Transaction_by_id_case(
            Transaction_id=Transaction_id
        )
    except BusinessError as error:
        raise HTTPException(
            status_code=error.http_status,
            detail=error.message
        )
