from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests
import structlog
from app.infrastructure.shared_resources.configure_shared_logger import configure_shared_logger, get_shared_logger

# Llamar a la función de configuración compartida UNA VEZ al inicio del servicio
# Esto aplica la configuración global de structlog.
configure_shared_logger()

# --- Paso de Inicialización: Obtener la instancia del Logger y Añadir Binds Específicos del Servicio ---
# Obtiene la instancia base del logger configurado.
# Añade binds que son constantes para este microservicio (nombre del servicio, componente, etc.)
logger = get_shared_logger().bind(service="transaction-service", component="http")


@dataclass
class HttpClient(object):
    api_host: str
    _session: Optional[requests.Session] = None  # type: ignore

    def __post_init__(self):
        if not self._session:
            self._session = requests.Session()

    def get(
        self,
        endpoint: str,
        query_params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        
        # --- 1. OBTENER el Trace ID del contexto de structlog ---
        # Accedemos al diccionario de variables del contexto actual.
        # El middleware ya se aseguró de que 'trace_id' esté allí para este request.
        current_context = structlog.contextvars.get_contextvars()
        current_trace_id = current_context.get('trace_id') # Obtenemos el valor del trace_id

        # --- 2. PREPARAR los encabezados para la propagación ---
        # Creamos un diccionario de encabezados.
        headers = {
            'Content-Type': 'application/json'
        }
        
        # Si tenemos un trace_id en el contexto, lo añadimos al encabezado de la petición saliente.
        # Es común usar 'X-Request-ID' o el estándar 'traceparent' (que es más complejo).
        if current_trace_id:
            headers["X-Request-ID"] = current_trace_id
            # Si usaras W3C Trace Context (traceparent), la lógica sería más compleja
            # para generar el encabezado 'traceparent' (incluye span id, flags, etc.)
            # headers["traceparent"] = generate_w3c_traceparent(current_trace_id, current_span_id)

        # --- 3. REALIZAR la llamada HTTP propagando los encabezados ---
        

        url = '{api_host}{endpoint}'.format(
            api_host=self.api_host,
            endpoint=endpoint,
        )

        # Opcional pero recomendado: Loggear que vas a hacer una llamada y con qué trace_id
        logger.info(
            "Preparing to call downstream service",
            downstream_service_url=url,
            # El trace_id ya se incluye automáticamente en este log debido al bind en el middleware
        )
        
        response = self._session.get(  # type: ignore
            url,
            headers=headers,
            params=query_params,
        )
        
         # Loggear la respuesta exitosa de la llamada saliente
        logger.info(
            "Successfully called downstream service",
            downstream_service_url=url,
            result=response.json(),
            # El trace_id se incluye automáticamente
        )
        
        response.raise_for_status()
        return response.json()

    def post(self, endpoint: str, payload: dict | str) -> Dict[str, Any]:
        headers = {
            'Content-Type': 'application/json',
        }
        url = '{api_host}{endpoint}'.format(
            api_host=self.api_host,
            endpoint=endpoint,
        )
        if isinstance(payload, dict):
            response = self._session.post(  # type: ignore
                url,
                headers=headers,
                json=payload,
            )
        elif isinstance(payload, str):
            response = self._session.post(  # type: ignore
                url,
                headers=headers,
                data=payload,
            )

        response.raise_for_status()
        return response.json()

    def put(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        headers = {
            'Content-Type': 'application/json',
        }
        url = '{api_host}{endpoint}'.format(
            api_host=self.api_host,
            endpoint=endpoint,
        )
        response = self._session.put(  # type: ignore
            url,
            headers=headers,
            json=payload,
        )
        response.raise_for_status()
        return response.json()
