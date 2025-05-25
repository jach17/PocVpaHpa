import pytest
from unittest.mock import AsyncMock
from app.core.application.ports.Users_adapter_port import UsersAdapterPort
from app.core.application.use_cases.adapters.Users_service_case import UsersUseCase


@pytest.mark.asyncio
async def test_get_Users_by_id_case_success():
    mock_adapter = AsyncMock(spec=UsersAdapterPort)
    mock_Users_data = {"id": "123", "name": "Test Users"}
    mock_adapter.get_Users_by_id.return_value = mock_Users_data

    Users_use_case = UsersUseCase(Users_service_adapter=mock_adapter)
    result = await Users_use_case.get_Users_by_id_case(Users_id="123")

    mock_adapter.get_Users_by_id.assert_awaited_once_with(Users_id="123")
    assert result == mock_Users_data


@pytest.mark.asyncio
async def test_get_Users_by_id_case_error_handling():
    mock_adapter = AsyncMock(spec=UsersAdapterPort)
    mock_adapter.get_Users_by_id.side_effect = Exception("API Error")

    Users_use_case = UsersUseCase(Users_service_adapter=mock_adapter)

    with pytest.raises(Exception) as exc_info:
        await Users_use_case.get_Users_by_id_case(Users_id="123")

    assert str(exc_info.value) == "API Error"
    mock_adapter.get_Users_by_id.assert_awaited_once_with(Users_id="123")