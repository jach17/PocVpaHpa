import pytest
from unittest.mock import MagicMock, create_autospec
from app.core.domain.services.TransactionRepository.Transaction_repository_service import TransactionRepositoryService
from app.core.domain.entities.TransactionRepository.Transaction import Transaction
from app.core.application.ports.database.Transaction_repository_db_port import TransactionRepositoryDBPort

@pytest.fixture
def mock_repo():
    return create_autospec(TransactionRepositoryDBPort, instance=True)

@pytest.fixture
def Transaction_service(mock_repo):
    return TransactionRepositoryService(repo=mock_repo)

@pytest.mark.asyncio
async def test_get_all_Transactions(Transaction_service, mock_repo):
    expected_Transactions = [MagicMock(), MagicMock()]
    mock_repo.get_all_Transactions.return_value = expected_Transactions

    result = await Transaction_service.get_all_Transactions()
    
    assert result == expected_Transactions
    mock_repo.get_all_Transactions.assert_awaited_once()

@pytest.mark.asyncio
async def test_get_Transaction_by_id(Transaction_service, mock_repo):
    test_id = 123
    expected_Transaction = MagicMock()
    mock_repo.get_Transaction_by_id.return_value = expected_Transaction

    result = await Transaction_service.get_Transaction_by_id(test_id)
    
    assert result == expected_Transaction
    mock_repo.get_Transaction_by_id.assert_awaited_once_with(test_id)

@pytest.mark.asyncio
async def test_update_Transaction(Transaction_service, mock_repo):
    test_id = "abc123"
    test_nombre = "Juan"
    test_telefono = "555-1234"
    expected_result = MagicMock()
    mock_repo.update_Transaction.return_value = expected_result

    result = await Transaction_service.update_Transaction(test_id, test_nombre, test_telefono)
    
    assert result == expected_result
    mock_repo.update_Transaction.assert_awaited_once_with(test_id, test_nombre, test_telefono)

@pytest.mark.asyncio
async def test_create_Transaction(Transaction_service, mock_repo):
    test_Transaction = Transaction(id=1, nombre="Maria", telefono="555-4321")
    expected_result = MagicMock()
    mock_repo.create_Transaction.return_value = expected_result

    result = await Transaction_service.create_Transaction(test_Transaction)
    
    assert result == expected_result
    mock_repo.create_Transaction.assert_awaited_once_with(test_Transaction)