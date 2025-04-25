import pytest
from unittest.mock import AsyncMock
from app.core.application.ports.Transaction_adapter_port import TransactionAdapterPort
from app.core.application.use_cases.adapters.Transaction_service_case import TransactionUseCase


@pytest.mark.asyncio
async def test_get_Transaction_by_id_case_success():
    mock_adapter = AsyncMock(spec=TransactionAdapterPort)
    mock_Transaction_data = {"id": "123", "name": "Test Transaction"}
    mock_adapter.get_Transaction_by_id.return_value = mock_Transaction_data

    Transaction_use_case = TransactionUseCase(Transaction_service_adapter=mock_adapter)
    result = await Transaction_use_case.get_Transaction_by_id_case(Transaction_id="123")

    mock_adapter.get_Transaction_by_id.assert_awaited_once_with(Transaction_id="123")
    assert result == mock_Transaction_data


@pytest.mark.asyncio
async def test_get_Transaction_by_id_case_error_handling():
    mock_adapter = AsyncMock(spec=TransactionAdapterPort)
    mock_adapter.get_Transaction_by_id.side_effect = Exception("API Error")

    Transaction_use_case = TransactionUseCase(Transaction_service_adapter=mock_adapter)

    with pytest.raises(Exception) as exc_info:
        await Transaction_use_case.get_Transaction_by_id_case(Transaction_id="123")

    assert str(exc_info.value) == "API Error"
    mock_adapter.get_Transaction_by_id.assert_awaited_once_with(Transaction_id="123")