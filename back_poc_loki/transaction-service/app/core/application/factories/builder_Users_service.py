from app.core.application.ports.Users_adapter_port import UsersAdapterPort
from app.core.application.use_cases.adapters.Users_service_case import (
    UsersUseCase
)
from app.infrastructure.adapters.Users_adapter_service import UsersAdapterService
from app.infrastructure.config.settings import settings
from app.infrastructure.http.http_client import HttpClient


def build_Users_adapter_service() -> UsersAdapterPort:
    return UsersAdapterService(
        http_client=HttpClient(api_host=settings.Users_BASE_URL)
    )


def builder_Users_adapter_use_case():
    http_client = HttpClient(
        api_host=settings.Users_BASE_URL
    )
    Users_adapter_service = UsersAdapterService(http_client)
    return UsersUseCase(Users_adapter_service)
