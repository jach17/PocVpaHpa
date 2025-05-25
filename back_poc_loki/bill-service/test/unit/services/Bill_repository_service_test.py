import pytest
from unittest.mock import MagicMock, create_autospec
from app.core.domain.services.BillRepository.Bill_repository_service import BillRepositoryService
from app.core.domain.entities.BillRepository.Bill import Bill
from app.core.application.ports.database.Bill_repository_db_port import BillRepositoryDBPort

@pytest.fixture
def mock_repo():
    return create_autospec(BillRepositoryDBPort, instance=True)

@pytest.fixture
def Bill_service(mock_repo):
    return BillRepositoryService(repo=mock_repo)

@pytest.mark.asyncio
async def test_get_all_Bills(Bill_service, mock_repo):
    expected_Bills = [MagicMock(), MagicMock()]
    mock_repo.get_all_Bills.return_value = expected_Bills

    result = await Bill_service.get_all_Bills()
    
    assert result == expected_Bills
    mock_repo.get_all_Bills.assert_awaited_once()

@pytest.mark.asyncio
async def test_get_Bill_by_id(Bill_service, mock_repo):
    test_id = 123
    expected_Bill = MagicMock()
    mock_repo.get_Bill_by_id.return_value = expected_Bill

    result = await Bill_service.get_Bill_by_id(test_id)
    
    assert result == expected_Bill
    mock_repo.get_Bill_by_id.assert_awaited_once_with(test_id)

@pytest.mark.asyncio
async def test_update_Bill(Bill_service, mock_repo):
    test_id = "abc123"
    test_nombre = "Juan"
    test_telefono = "555-1234"
    expected_result = MagicMock()
    mock_repo.update_Bill.return_value = expected_result

    result = await Bill_service.update_Bill(test_id, test_nombre, test_telefono)
    
    assert result == expected_result
    mock_repo.update_Bill.assert_awaited_once_with(test_id, test_nombre, test_telefono)

@pytest.mark.asyncio
async def test_create_Bill(Bill_service, mock_repo):
    test_Bill = Bill(id=1, nombre="Maria", telefono="555-4321")
    expected_result = MagicMock()
    mock_repo.create_Bill.return_value = expected_result

    result = await Bill_service.create_Bill(test_Bill)
    
    assert result == expected_result
    mock_repo.create_Bill.assert_awaited_once_with(test_Bill)