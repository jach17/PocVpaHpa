import logging
import time
import uuid
import structlog

from fastapi import FastAPI, Request, status
from contextlib import asynccontextmanager

import uvicorn
from app.infrastructure.database.session import engine
from app.infrastructure.api.routers.healthcheck_route import (
    router as health_router
)
from app.infrastructure.api.routers.Transaction_repository_router import (
    router as Transaction_repository_router
)
from app.infrastructure.api.routers.Users_adapter_router import (
    router as Transaction_adapter_router
)
from app.infrastructure.shared_resources.configure_shared_logger import PrometheusMiddleware, metrics, setting_otlp
from app.infrastructure.config.settings import settings

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

# Setting prometheus metrics middleware
app.add_middleware(PrometheusMiddleware, app_name=settings.APP_NAME)
app.add_route("/metrics", metrics)

setting_otlp(app, settings.APP_NAME, settings.OTLP_GRPC_ENDPOINT)

class EndpointFilter(logging.Filter):
    # Uvicorn endpoint access log filter
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("GET /metrics") == -1

logging.getLogger("uvicorn.access").addFilter(EndpointFilter())


def set_logging_config():
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"][
        "fmt"
    ] = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s"
    

set_logging_config()


# app.include_router(health_router)
# app.include_router(Transaction_repository_router)
app.include_router(Transaction_adapter_router)
