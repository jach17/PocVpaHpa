from unittest.mock import patch
from app.core.application.factories.builder_Users_service import build_Users_adapter_service, builder_Users_adapter_use_case
from app.infrastructure.adapters.Users_adapter_service import UsersAdapterService
from app.core.application.use_cases.adapters.Users_service_case import UsersUseCase


def test_build_Transaction_adapter_service():
    with patch("app.core.application.factories.builder_Users_service.settings") as mock_settings:
        mock_settings.Users_BASE_URL = "http://test-api"

        adapter = build_Users_adapter_service()

        assert isinstance(adapter, UsersAdapterService)
        assert adapter._http_client.api_host == "http://test-api"

def test_builder_Users_adapter_use_case():
    with patch("app.core.application.factories.builder_Users_service.settings") as mock_settings:
        mock_settings.Users_BASE_URL = "http://test-api"

        use_case = builder_Users_adapter_use_case()

        assert isinstance(use_case, UsersUseCase)
        assert isinstance(use_case.Users_service_adapter, UsersAdapterService)
        assert use_case.Users_service_adapter._http_client.api_host == "http://test-api"