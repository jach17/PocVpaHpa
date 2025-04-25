from fastapi import APIRouter, HTTPException, requests
import structlog

from app.core.application.factories.builder_Empty_service import (
    builder_Empty_adapter_use_case
)
from app.infrastructure.api.schemas.exceptions import BusinessError
from app.infrastructure.api.schemas.User_schema import EmptyResponseService
from app.infrastructure.shared_resources.configure_shared_logger import get_shared_logger


router = APIRouter(
    prefix="/api/v1/empty",
    tags=["Empty"]
)


@router.get(
    path="",
    response_model=EmptyResponseService
)
async def get_Empty_by_id(
        Empty_id: str
):
    try:
        use_case = builder_Empty_adapter_use_case()
        response = await use_case.get_Empty_by_id_case(
            Empty_id=Empty_id
        )
    
        return response # O procesar la respuesta como necesites

    except BusinessError as error:
        raise HTTPException(
            status_code=error.http_status,
            detail=error.message
        )


def call_downstream_service(resource_id: str):
    """
    Ejemplo de una función que realiza una llamada saliente
    a otro microservicio y propaga el trace_id.
    """
    # --- 1. OBTENER el Trace ID del contexto de structlog ---
    # Accedemos al diccionario de variables del contexto actual.
    # El middleware ya se aseguró de que 'trace_id' esté allí para este request.
    current_context = structlog.contextvars.get_contextvars()
    current_trace_id = current_context.get('trace_id') # Obtenemos el valor del trace_id

    # Opcional pero recomendado: Loggear que vas a hacer una llamada y con qué trace_id
    logger.info(
        "Preparing to call downstream service",
        downstream_service_url=f"http://downstream-service/{resource_id}",
        # El trace_id ya se incluye automáticamente en este log debido al bind en el middleware
    )

    # --- 2. PREPARAR los encabezados para la propagación ---
    # Creamos un diccionario de encabezados.
    headers = {}
    # Si tenemos un trace_id en el contexto, lo añadimos al encabezado de la petición saliente.
    # Es común usar 'X-Request-ID' o el estándar 'traceparent' (que es más complejo).
    if current_trace_id:
        headers["X-Request-ID"] = current_trace_id
        # Si usaras W3C Trace Context (traceparent), la lógica sería más compleja
        # para generar el encabezado 'traceparent' (incluye span id, flags, etc.)
        # headers["traceparent"] = generate_w3c_traceparent(current_trace_id, current_span_id)


    target_url = f"http://downstream-service/resource/{resource_id}" # URL del servicio destino

    # --- 3. REALIZAR la llamada HTTP propagando los encabezados ---
    try:
        # Realiza la petición saliente, incluyendo los encabezados preparados
        response = requests.get(target_url, headers=headers)

        # Lanza una excepción si la respuesta tiene un código de error (4xx o 5xx)
        response.raise_for_status()

        # Loggear la respuesta exitosa de la llamada saliente
        logger.info(
            "Successfully called downstream service",
            downstream_service_url=target_url,
            status_code=response.status_code,
            # El trace_id se incluye automáticamente
        )

        return response.json() # O procesar la respuesta como necesites

    except requests.exceptions.RequestException as e:
        # Loggear si la llamada saliente falla
        logger.error(
            "Failed to call downstream service",
            downstream_service_url=target_url,
            exc_info=True, # Incluir detalles de la excepción en el log
            # El trace_id se incluye automáticamente
        )
        # Manejar el error, quizás relanzando la excepción o devolviendo un error apropiado
        raise e # Relanzar para que sea manejado por el llamador o middleware superior
