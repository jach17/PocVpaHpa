import logging
import random
import time
from fastapi import APIRouter, HTTPException, Response, requests
import structlog

from app.core.application.factories.builder_Users_service import (
    builder_Users_adapter_use_case
)
from app.infrastructure.api.schemas.exceptions import BusinessError
from app.infrastructure.api.schemas.Transaction_schema import UsersResponseService


router = APIRouter(
    prefix="/api/v1/transaction",
    tags=["Users"]
)

@router.get("/random_sleep")
async def random_sleep(response: Response):
    time.sleep(random.randint(0, 5))
    logging.error("random sleep")
    return {"path": "/random_sleep"}

@router.get(
    path="/user",
    response_model=UsersResponseService
)
async def get_Users_by_id(
        Users_id: str
):
    try:
        logging.error(f"Transaction router - Begin transaction-service {Users_id}")
        
        use_case = builder_Users_adapter_use_case()
        response = await use_case.get_Users_by_id_case(
            Users_id=Users_id
        )
        
        logging.error(f"Transaction router - End transaction-service - {response}")

        return response # O procesar la respuesta como necesites

    except BusinessError as error:
        raise HTTPException(
            status_code=error.http_status,
            detail=error.message
        )
