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


@router.get(
    path="",
    response_model=EmptyResponseService
)
async def get_Empty_by_id(
        Empty_id: str
):
    try:
        use_case = builder_Empty_adapter_use_case()
        response = await use_case.get_Empty_by_id_case(
            Empty_id=Empty_id
        )
    
        return response # O procesar la respuesta como necesites

    except BusinessError as error:
        raise HTTPException(
            status_code=error.http_status,
            detail=error.message
        )