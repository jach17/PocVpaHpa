from sqlalchemy import select
from app.core.application.ports.database.Bill_repository_db_port import (
    BillRepositoryDBPort
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.domain.entities.BillRepository.Bill import Bill
from app.infrastructure.database.models.Bill_model import BillModel


class BillRepository(BillRepositoryDBPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_Bills(self):
        print("Repository: OK")
        print("Repository query starts")
        try:
            result = await self.session.execute(select(BillModel))
            Bills = result.scalars().all()
            print(f"Repository query ends - {Bills}")
            return [
                Bill(id=u.id, nombre=u.nombre, telefono=u.telefono)
                for u in Bills
            ]
        except Exception as e:
            print(f"Exception on get all Bills - {e}")
            raise RuntimeError(f"DB error: {e}") from e

    async def get_Bill_by_id(self, Bill_id: int):
        result = await self.session.get(BillModel, Bill_id)
        return Bill(
            id=result.id,
            nombre=result.nombre,
            telefono=result.telefono
            ) if result else None

    async def create_Bill(self, Bill_to_create: Bill):
        db_Bill = BillModel(nombre=Bill_to_create.nombre, telefono=Bill_to_create.telefono)
        self.session.add(db_Bill)
        await self.session.commit()
        await self.session.refresh(db_Bill)
        return Bill(
            id=db_Bill.id,
            nombre=db_Bill.nombre,
            telefono=db_Bill.telefono
            )

    async def update_Bill(self, id: str, nombre: str, telefono: str):
        print("Repository: OK")
        print("Repository query starts")
        try:
            result = await self.session.get(BillModel, int(id))
            if not result:
                return None
            result.nombre = nombre
            result.telefono = telefono
            await self.session.commit()
            await self.session.refresh(result)
            return result
        except Exception as e:
            print(f"Exception on update Bill - {e}")
            raise RuntimeError(f"DB error: {e}") from e
