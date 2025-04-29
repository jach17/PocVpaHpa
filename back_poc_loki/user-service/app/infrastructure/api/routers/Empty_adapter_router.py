import json
import logging
import random
import time
from fastapi import APIRouter, HTTPException, Response, requests
import structlog

from app.core.application.factories.builder_Empty_service import (
    builder_Empty_adapter_use_case
)
from app.infrastructure.api.schemas.exceptions import BusinessError
from app.infrastructure.api.schemas.User_schema import EmptyResponseService


router = APIRouter(
    prefix="/api/v1/empty",
    tags=["Empty"]
)


@router.get("/random_sleep")
async def random_sleep(response: Response):
    time.sleep(random.randint(0, 5))
    logging.error("random sleep")
    return {"path": "/random_sleep"}

@router.get(
    path="",
    response_model=EmptyResponseService
)
async def get_Empty_by_id(
        Empty_id: str
):
    try:
        logging.error(f"User router - Begin user-service {Empty_id}")
        use_case = builder_Empty_adapter_use_case()
        response = await use_case.get_Empty_by_id_case(
            Empty_id=Empty_id
        )
    
        logging.error(f"User router - End user-service - {response}")
        return response # O procesar la respuesta como necesites

    except BusinessError as error:
        raise HTTPException(
            status_code=error.http_status,
            detail=error.message
        )