import time
import uuid
import structlog

from fastapi import FastAPI, Request, status
from contextlib import asynccontextmanager
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
from app.infrastructure.shared_resources.configure_shared_logger import configure_shared_logger, get_shared_logger

# Llamar a la función de configuración compartida UNA VEZ al inicio del servicio
# Esto aplica la configuración global de structlog.
configure_shared_logger()

# --- Paso de Inicialización: Obtener la instancia del Logger y Añadir Binds Específicos del Servicio ---
# Obtiene la instancia base del logger configurado.
# Añade binds que son constantes para este microservicio (nombre del servicio, componente, etc.)
logger = get_shared_logger().bind(service="transaction-service", component="http")


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

@app.middleware("http")
async def add_trace_id_and_log_requests(request: Request, call_next):
    """
    Middleware para añadir/extraer Trace ID y loggear peticiones.
    Se ejecuta para cada petición HTTP que llega a este servicio.
    """
    # --- RECIBIR / EXTRAER o GENERAR el Trace ID ---
    # Busca si un servicio upstream envió un Trace ID en un encabezado conocido (ej. X-Request-ID).
    # Si no existe (este servicio es el origen de la traza o el upstream no propagó), genera uno nuevo.
    # Usar X-Request-ID es común para simpleza, pero W3C Trace Context (encabezado 'traceparent') es el estándar.
    # Puedes añadir lógica para traceparent si lo necesitas.
    trace_id = request.headers.get("x-request-id") or str(uuid.uuid4())

    # --- BINDEAR el Trace ID al contexto de structlog para esta petición ---
    # Esto hace que 'trace_id' esté disponible automáticamente en el diccionario
    # de todos los logs que se generen con el logger dentro de este request.
    # Este bind es crucial para correlacionar logs.
    structlog.contextvars.bind_contextvars(trace_id=trace_id)

    start_time = time.time()
    response = None # Inicializar la variable response

    try:
        # --- Procesar la Petición ---
        # Pasar la petición al siguiente middleware o al manejador de ruta final.
        # Todo el código que se ejecute ahora (endpoints, llamadas a otras funciones)
        # usará el logger con el trace_id bindeado.
        response = await call_next(request)

        # --- Loggear el Resultado de la Petición (éxito o error manejado) ---
        duration = time.time() - start_time
        # Usa el logger. El trace_id y los binds del servicio ya están en el contexto.
        logger.info(
            "Request handled",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration=round(duration * 1000, 2),  # duración en milisegundos
        )
        return response

    except Exception as e:
        # --- Loggear Excepciones No Manejadas ---
        # Captura excepciones que no fueron manejadas en otro lugar y loggéalas.
        # El trace_id y los binds del servicio ya están en el contexto.
        duration = time.time() - start_time
        logger.error(
            "Request failed due to unhandled exception",
            method=request.method,
            path=request.url.path,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, # Asigna un 500 para este log de error
            duration=round(duration * 1000, 2),
            exc_info=True # Incluye la información de la excepción y el traceback en el log
        )
        # MUY IMPORTANTE: Relanza la excepción para que FastAPI pueda manejarla
        # y devolver una respuesta HTTP 500 apropiada al cliente.
        raise e

    finally:
        # --- DESBINDEAR el Trace ID ---
        # Limpia el contextvar del trace_id al finalizar la petición.
        # Esto es CRÍTICO para evitar que el trace_id de una petición
        # se "filtre" y aparezca en los logs de una petición posterior
        # procesada por el mismo worker.
        structlog.contextvars.unbind_contextvars("trace_id")


# app.include_router(health_router)
# app.include_router(Transaction_repository_router)
app.include_router(Transaction_adapter_router)
