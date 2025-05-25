from unittest.mock import patch
from app.core.application.factories.builder_Transaction_service import build_Transaction_adapter_service, builder_Transaction_adapter_use_case
from app.infrastructure.adapters.Transaction_adapter_service import TransactionAdapterService
from app.core.application.use_cases.adapters.Transaction_service_case import TransactionUseCase


def test_build_Bill_adapter_service():
    with patch("app.core.application.factories.builder_Transaction_service.settings") as mock_settings:
        mock_settings.Transaction_BASE_URL = "http://test-api"

        adapter = build_Transaction_adapter_service()

        assert isinstance(adapter, TransactionAdapterService)
        assert adapter._http_client.api_host == "http://test-api"

def test_builder_Transaction_adapter_use_case():
    with patch("app.core.application.factories.builder_Transaction_service.settings") as mock_settings:
        mock_settings.Transaction_BASE_URL = "http://test-api"

        use_case = builder_Transaction_adapter_use_case()

        assert isinstance(use_case, TransactionUseCase)
        assert isinstance(use_case.Transaction_service_adapter, TransactionAdapterService)
        assert use_case.Transaction_service_adapter._http_client.api_host == "http://test-api"