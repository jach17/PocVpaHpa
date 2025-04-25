import json
from pydantic.dataclasses import dataclass

from app.core.application.ports.database.User_repository_db_port import (
    UserRepositoryDBPort
)
from app.core.application.ports.services.User_repository_service_port import (
    UserRepositoryServicePort
)
from app.core.domain.entities.UserRepository.User import User


@dataclass(config=dict(arbitrary_types_allowed=True))
class UserRepositoryService(UserRepositoryServicePort):
    repo: UserRepositoryDBPort

    async def get_all_Users(self):
        print("Service implementation: OK")
        return await self.repo.get_all_Users()

    async def get_User_by_id(self, User_id: int):
        print("Service implementation: OK")
        return await self.repo.get_User_by_id(User_id)

    async def update_User(self, id: str, nombre: str, telefono: str):
        print("Service implementation: OK")
        return await self.repo.update_User(id, nombre, telefono)

    async def create_User(self, User: User):
        print("Service implementation: OK")
        print(f"Request: {json.dumps(User.__dict__, indent=2)}")
        return await self.repo.create_User(User)
