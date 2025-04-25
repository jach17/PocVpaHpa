# shared_logger.py

import logging
import sys
import structlog
import structlog.contextvars # Necesitas importar esto para que structlog sepa usar contextvars

def configure_shared_logger():
    """
    Configura el logger compartido usando structlog.
    Debe llamarse una vez al inicio de CADA microservicio.
    """
    # Configura el logger base del standard library. structlog usa esto por debajo.
    logging.basicConfig(
        format="%(message)s", # structlog renderizará a JSON en este formato
        stream=sys.stdout,    # Enviar logs a la salida estándar
        level=logging.INFO    # Nivel mínimo de logs a procesar
    )

    # Configura structlog con los procesadores deseados
    structlog.configure(
        processors=[
            # Este procesador fusiona los contextvars (como trace_id) en el diccionario del evento de log
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,       # Añade el nivel del log (info, error, etc.)
            structlog.processors.TimeStamper(fmt="iso"), # Añade la marca de tiempo ISO
            # Puedes añadir procesadores para filtrar campos, renombrar, etc., aquí
            structlog.processors.StackInfoRenderer(), # Opcional: añade stack info en errores
            structlog.processors.format_exc_info,     # Opcional: añade info de excepción
            # Este es el procesador final que convierte el diccionario a JSON
            structlog.processors.JSONRenderer()
        ],
        logger_factory=structlog.stdlib.LoggerFactory(), # Usa loggers del standard library
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO), # Envuelve para añadir filtrado por nivel
        cache_logger_on_first_use=True, # Cachea el logger para rendimiento
    )

def get_shared_logger():
    """
    Obtiene una instancia del logger configurado por structlog.
    """
    # Retorna la instancia base del logger.
    # Los binds específicos (servicio, componente) se harán después de importarlo.
    return structlog.get_logger()

# La lógica de bind_contextvars() NO va aquí, ya que es específica de cada petición.