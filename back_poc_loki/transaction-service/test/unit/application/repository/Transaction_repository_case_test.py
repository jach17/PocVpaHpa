import pytest
from unittest.mock import MagicMock, create_autospec
from app.core.application.ports.services.Transaction_repository_service_port import TransactionRepositoryServicePort
from app.core.domain.entities.TransactionRepository.Transaction import Transaction
from app.core.application.use_cases.repository.Transaction_repository_case import (
    get_all_Transactions_case, get_Transaction_case, update_Transaction_case, create_Transaction_case
)

@pytest.fixture
def mock_service():
    return create_autospec(TransactionRepositoryServicePort, instance=True)

@pytest.mark.asyncio
async def test_get_all_Transactions_case(mock_service):
    expected_result = [MagicMock(), MagicMock()]
    mock_service.get_all_Transactions.return_value = expected_result

    result = await get_all_Transactions_case(mock_service)

    assert result == expected_result
    mock_service.get_all_Transactions.assert_awaited_once()

@pytest.mark.asyncio
async def test_get_Transaction_case(mock_service):
    test_id = 123
    expected_Transaction = MagicMock()
    mock_service.get_Transaction_by_id.return_value = expected_Transaction

    result = await get_Transaction_case(mock_service, test_id)

    assert result == expected_Transaction
    mock_service.get_Transaction_by_id.assert_awaited_once_with(test_id)

@pytest.mark.asyncio
async def test_update_Transaction_case(mock_service):
    test_data = {
        "id": "Transaction-123",
        "nombre": "Ana",
        "telefono": "555-9876"
    }
    mock_service.update_Transaction.return_value = MagicMock()

    result = await update_Transaction_case(
        mock_service,
        test_data["id"],
        test_data["nombre"],
        test_data["telefono"]
    )

    assert result is not None
    mock_service.update_Transaction.assert_awaited_once_with(
        test_data["id"],
        test_data["nombre"],
        test_data["telefono"]
    )

@pytest.mark.asyncio
async def test_create_Transaction_case(mock_service):
    test_nombre = "Carlos"
    test_telefono = "555-5555"

    mock_service.create_Transaction.return_value = MagicMock()

    result = await create_Transaction_case(mock_service, test_nombre, test_telefono)

    assert result is not None
    mock_service.create_Transaction.assert_awaited_once()

    called_Transaction = mock_service.create_Transaction.call_args.args[0]
    assert isinstance(called_Transaction, Transaction)
    assert called_Transaction.nombre == test_nombre
    assert called_Transaction.telefono == test_telefono