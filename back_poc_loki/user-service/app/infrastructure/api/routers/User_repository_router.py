from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.core.application.ports.services.User_repository_service_port import (
    UserRepositoryServicePort
)
from app.infrastructure.api.routers.dependencies import (
    get_User_repository_service
)
from app.core.application.use_cases.repository.User_repository_case import (
    create_User_case,
    get_all_Users_case,
    update_User_case
)
from app.infrastructure.api.schemas.User_schema import UserCreate, UserResponse


router = APIRouter(
    prefix="/api/v1/repo/repository",
    tags=["Users"]
)


@router.post(
    path="/",
    response_model=UserResponse
)
async def create_User(
    User: UserCreate,
    repository: UserRepositoryServicePort = Depends(
        get_User_repository_service
    )
):
    print("Router: OK")
    return await create_User_case(
        User_service_repository=repository,
        nombre=User.nombre,
        telefono=User.telefono
    )


@router.put(
    "/{User_id}",
    response_model=UserResponse
)
async def update_User(
    User: UserCreate,
    User_id: str,
    repository: UserRepositoryServicePort = Depends(
        get_User_repository_service
    )
):
    print("Router: OK")
    updated = await update_User_case(
        User_service_repository=repository,
        id=User_id,
        nombre=User.nombre,
        telefono=User.telefono
    )
    if updated:
        return updated
    return JSONResponse(status_code=404, content={"detail": "User not found"})


@router.get("/")
async def list_Users(
    repository: UserRepositoryServicePort = Depends(
        get_User_repository_service
    )
):
    print("Router: OK")
    return await get_all_Users_case(User_service_repository=repository)
