import pytest
from unittest.mock import AsyncMock
from app.core.application.ports.Empty_adapter_port import EmptyAdapterPort
from app.core.application.use_cases.adapters.Empty_service_case import EmptyUseCase


@pytest.mark.asyncio
async def test_get_Empty_by_id_case_success():
    mock_adapter = AsyncMock(spec=EmptyAdapterPort)
    mock_Empty_data = {"id": "123", "name": "Test Empty"}
    mock_adapter.get_Empty_by_id.return_value = mock_Empty_data

    Empty_use_case = EmptyUseCase(Empty_service_adapter=mock_adapter)
    result = await Empty_use_case.get_Empty_by_id_case(Empty_id="123")

    mock_adapter.get_Empty_by_id.assert_awaited_once_with(Empty_id="123")
    assert result == mock_Empty_data


@pytest.mark.asyncio
async def test_get_Empty_by_id_case_error_handling():
    mock_adapter = AsyncMock(spec=EmptyAdapterPort)
    mock_adapter.get_Empty_by_id.side_effect = Exception("API Error")

    Empty_use_case = EmptyUseCase(Empty_service_adapter=mock_adapter)

    with pytest.raises(Exception) as exc_info:
        await Empty_use_case.get_Empty_by_id_case(Empty_id="123")

    assert str(exc_info.value) == "API Error"
    mock_adapter.get_Empty_by_id.assert_awaited_once_with(Empty_id="123")