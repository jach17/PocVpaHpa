from contextlib import asynccontextmanager
from app.infrastructure.database.repositories.healthcheck_repository import (
    HealthCheckRepository
)
from app.infrastructure.adapters.healthcheck_adapter import HealthCheckAdapter
from app.infrastructure.database.session import get_db


class HealthCheckFactory:
    @staticmethod
    @asynccontextmanager
    async def create():
        async for session in get_db():
            try:
                repository = HealthCheckRepository(session)
                yield HealthCheckAdapter(repository)
                await session.commit()  # Commit para operaciones exitosas
            except Exception as e:
                await session.rollback()  # Rollback en caso de error
                raise e
            finally:
                await session.close()  # Cierre seguro de la conexión
