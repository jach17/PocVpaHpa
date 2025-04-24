import math
import time
from fastapi import FastAPI, Request, status # Import status for error logging
import uvicorn
import structlog
import uuid

# --- Paso de Inicialización: Importar y Configurar el Logger Compartido ---
from utils.configure_shared_logger import configure_shared_logger, get_shared_logger

# Llamar a la función de configuración compartida UNA VEZ al inicio del servicio
# Esto aplica la configuración global de structlog.
configure_shared_logger()

# --- Paso de Inicialización: Obtener la instancia del Logger y Añadir Binds Específicos del Servicio ---
# Obtiene la instancia base del logger configurado.
# Añade binds que son constantes para este microservicio (nombre del servicio, componente, etc.)
logger = get_shared_logger().bind(service="ping-service", component="http")


app = FastAPI()



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





# --- Your Endpoint Remains Largely the Same ---
@app.get("/ping")
def ping():
    # Any log message from 'logger' inside this function will automatically
    # include the 'trace_id' because it was bound in the middleware.
    logger.info("Processing ping request inside endpoint") # This log will have trace_id

    [math.sqrt(i) for i in range(10000)]
    time.sleep(0.05)

    logger.info("Finished processing ping request") # This log will also have trace_id

    return {"message": "pong"}

if __name__ == "__main__":
    # log_config=None is important! It disables Uvicorn's default logging
    # so you only get the logs from your structlog configuration.
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_config=None)