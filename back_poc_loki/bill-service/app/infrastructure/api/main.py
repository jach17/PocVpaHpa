from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.infrastructure.database.session import engine
from app.infrastructure.api.routers.healthcheck_route import (
    router as health_router
)
from app.infrastructure.api.routers.Bill_repository_router import (
    router as Bill_repository_router
)
from app.infrastructure.api.routers.Transaction_adapter_router import (
    router as Bill_adapter_router
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Aquí iría cualquier inicialización necesaria al startup
    yield
    # Limpieza durante el shutdown
    await engine.dispose()

app = FastAPI(
    title="Arquetipo FastAPI",
    version="0.1.0",
    lifespan=lifespan
)

#app.include_router(health_router)
#app.include_router(Bill_repository_router)
app.include_router(Bill_adapter_router)
