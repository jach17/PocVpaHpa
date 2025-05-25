from unittest.mock import patch
from app.core.application.factories.builder_Empty_service import build_Empty_adapter_service, builder_Empty_adapter_use_case
from app.infrastructure.adapters.Empty_adapter_service import EmptyAdapterService
from app.core.application.use_cases.adapters.Empty_service_case import EmptyUseCase


def test_build_User_adapter_service():
    with patch("app.core.application.factories.builder_Empty_service.settings") as mock_settings:
        mock_settings.Empty_BASE_URL = "http://test-api"

        adapter = build_Empty_adapter_service()

        assert isinstance(adapter, EmptyAdapterService)
        assert adapter._http_client.api_host == "http://test-api"

def test_builder_Empty_adapter_use_case():
    with patch("app.core.application.factories.builder_Empty_service.settings") as mock_settings:
        mock_settings.Empty_BASE_URL = "http://test-api"

        use_case = builder_Empty_adapter_use_case()

        assert isinstance(use_case, EmptyUseCase)
        assert isinstance(use_case.Empty_service_adapter, EmptyAdapterService)
        assert use_case.Empty_service_adapter._http_client.api_host == "http://test-api"