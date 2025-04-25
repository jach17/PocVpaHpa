import json
from app.core.application.ports.services.User_repository_service_port import (
    UserRepositoryServicePort
)
from app.core.domain.entities.UserRepository.User import User


async def get_all_Users_case(
    User_service_repository: UserRepositoryServicePort
):
    print("Use cases: OK")
    return await User_service_repository.get_all_Users()


async def get_User_case(
    User_service_repository: UserRepositoryServicePort,
    User_id: int
):
    print("Use cases: OK")
    return await User_service_repository.get_User_by_id(User_id)


async def update_User_case(
    User_service_repository: UserRepositoryServicePort,
    id: str,
    nombre: str,
    telefono: str
):
    print("Use cases: OK")
    return await User_service_repository.update_User(id, nombre, telefono)


async def create_User_case(
    User_service_repository: UserRepositoryServicePort,
    nombre: str,
    telefono: str
):
    obj = User(id=0, nombre=nombre, telefono=telefono)
    print("Use case: OK")
    print(f"Request: {json.dumps(obj.__dict__, indent=2)}")
    return await User_service_repository.create_User(obj)
