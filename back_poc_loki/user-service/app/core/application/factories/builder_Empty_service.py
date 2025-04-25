from app.core.application.ports.Empty_adapter_port import EmptyAdapterPort
from app.core.application.use_cases.adapters.Empty_service_case import (
    EmptyUseCase
)
from app.infrastructure.adapters.Empty_adapter_service import EmptyAdapterService
from app.infrastructure.config.settings import settings
from app.infrastructure.http.http_client import HttpClient


def build_Empty_adapter_service() -> EmptyAdapterPort:
    return EmptyAdapterService(
        http_client=HttpClient(api_host=settings.Empty_BASE_URL)
    )


def builder_Empty_adapter_use_case():
    http_client = HttpClient(
        api_host=settings.Empty_BASE_URL
    )
    Empty_adapter_service = EmptyAdapterService(http_client)
    return EmptyUseCase(Empty_adapter_service)
