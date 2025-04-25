from app.core.application.ports.Transaction_adapter_port import TransactionAdapterPort
from app.core.application.use_cases.adapters.Transaction_service_case import (
    TransactionUseCase
)
from app.infrastructure.adapters.Transaction_adapter_service import TransactionAdapterService
from app.infrastructure.config.settings import settings
from app.infrastructure.http.http_client import HttpClient


def build_Transaction_adapter_service() -> TransactionAdapterPort:
    return TransactionAdapterService(
        http_client=HttpClient(api_host=settings.Transaction_BASE_URL)
    )


def builder_Transaction_adapter_use_case():
    http_client = HttpClient(
        api_host=settings.Transaction_BASE_URL
    )
    Transaction_adapter_service = TransactionAdapterService(http_client)
    return TransactionUseCase(Transaction_adapter_service)
