from sqlalchemy import select
from app.core.application.ports.database.Transaction_repository_db_port import (
    TransactionRepositoryDBPort
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.domain.entities.TransactionRepository.Transaction import Transaction
from app.infrastructure.database.models.Transaction_model import TransactionModel


class TransactionRepository(TransactionRepositoryDBPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_Transactions(self):
        print("Repository: OK")
        print("Repository query starts")
        try:
            result = await self.session.execute(select(TransactionModel))
            Transactions = result.scalars().all()
            print(f"Repository query ends - {Transactions}")
            return [
                Transaction(id=u.id, nombre=u.nombre, telefono=u.telefono)
                for u in Transactions
            ]
        except Exception as e:
            print(f"Exception on get all Transactions - {e}")
            raise RuntimeError(f"DB error: {e}") from e

    async def get_Transaction_by_id(self, Transaction_id: int):
        result = await self.session.get(TransactionModel, Transaction_id)
        return Transaction(
            id=result.id,
            nombre=result.nombre,
            telefono=result.telefono
            ) if result else None

    async def create_Transaction(self, Transaction_to_create: Transaction):
        db_Transaction = TransactionModel(nombre=Transaction_to_create.nombre, telefono=Transaction_to_create.telefono)
        self.session.add(db_Transaction)
        await self.session.commit()
        await self.session.refresh(db_Transaction)
        return Transaction(
            id=db_Transaction.id,
            nombre=db_Transaction.nombre,
            telefono=db_Transaction.telefono
            )

    async def update_Transaction(self, id: str, nombre: str, telefono: str):
        print("Repository: OK")
        print("Repository query starts")
        try:
            result = await self.session.get(TransactionModel, int(id))
            if not result:
                return None
            result.nombre = nombre
            result.telefono = telefono
            await self.session.commit()
            await self.session.refresh(result)
            return result
        except Exception as e:
            print(f"Exception on update Transaction - {e}")
            raise RuntimeError(f"DB error: {e}") from e
