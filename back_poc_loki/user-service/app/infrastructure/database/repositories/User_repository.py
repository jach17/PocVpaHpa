from sqlalchemy import select
from app.core.application.ports.database.User_repository_db_port import (
    UserRepositoryDBPort
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.domain.entities.UserRepository.User import User
from app.infrastructure.database.models.User_model import UserModel


class UserRepository(UserRepositoryDBPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_Users(self):
        print("Repository: OK")
        print("Repository query starts")
        try:
            result = await self.session.execute(select(UserModel))
            Users = result.scalars().all()
            print(f"Repository query ends - {Users}")
            return [
                User(id=u.id, nombre=u.nombre, telefono=u.telefono)
                for u in Users
            ]
        except Exception as e:
            print(f"Exception on get all Users - {e}")
            raise RuntimeError(f"DB error: {e}") from e

    async def get_User_by_id(self, User_id: int):
        result = await self.session.get(UserModel, User_id)
        return User(
            id=result.id,
            nombre=result.nombre,
            telefono=result.telefono
            ) if result else None

    async def create_User(self, User_to_create: User):
        db_User = UserModel(nombre=User_to_create.nombre, telefono=User_to_create.telefono)
        self.session.add(db_User)
        await self.session.commit()
        await self.session.refresh(db_User)
        return User(
            id=db_User.id,
            nombre=db_User.nombre,
            telefono=db_User.telefono
            )

    async def update_User(self, id: str, nombre: str, telefono: str):
        print("Repository: OK")
        print("Repository query starts")
        try:
            result = await self.session.get(UserModel, int(id))
            if not result:
                return None
            result.nombre = nombre
            result.telefono = telefono
            await self.session.commit()
            await self.session.refresh(result)
            return result
        except Exception as e:
            print(f"Exception on update User - {e}")
            raise RuntimeError(f"DB error: {e}") from e
