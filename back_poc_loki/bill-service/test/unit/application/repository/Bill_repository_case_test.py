import pytest
from unittest.mock import MagicMock, create_autospec
from app.core.application.ports.services.Bill_repository_service_port import BillRepositoryServicePort
from app.core.domain.entities.BillRepository.Bill import Bill
from app.core.application.use_cases.repository.Bill_repository_case import (
    get_all_Bills_case, get_Bill_case, update_Bill_case, create_Bill_case
)

@pytest.fixture
def mock_service():
    return create_autospec(BillRepositoryServicePort, instance=True)

@pytest.mark.asyncio
async def test_get_all_Bills_case(mock_service):
    expected_result = [MagicMock(), MagicMock()]
    mock_service.get_all_Bills.return_value = expected_result

    result = await get_all_Bills_case(mock_service)

    assert result == expected_result
    mock_service.get_all_Bills.assert_awaited_once()

@pytest.mark.asyncio
async def test_get_Bill_case(mock_service):
    test_id = 123
    expected_Bill = MagicMock()
    mock_service.get_Bill_by_id.return_value = expected_Bill

    result = await get_Bill_case(mock_service, test_id)

    assert result == expected_Bill
    mock_service.get_Bill_by_id.assert_awaited_once_with(test_id)

@pytest.mark.asyncio
async def test_update_Bill_case(mock_service):
    test_data = {
        "id": "Bill-123",
        "nombre": "Ana",
        "telefono": "555-9876"
    }
    mock_service.update_Bill.return_value = MagicMock()

    result = await update_Bill_case(
        mock_service,
        test_data["id"],
        test_data["nombre"],
        test_data["telefono"]
    )

    assert result is not None
    mock_service.update_Bill.assert_awaited_once_with(
        test_data["id"],
        test_data["nombre"],
        test_data["telefono"]
    )

@pytest.mark.asyncio
async def test_create_Bill_case(mock_service):
    test_nombre = "Carlos"
    test_telefono = "555-5555"

    mock_service.create_Bill.return_value = MagicMock()

    result = await create_Bill_case(mock_service, test_nombre, test_telefono)

    assert result is not None
    mock_service.create_Bill.assert_awaited_once()

    called_Bill = mock_service.create_Bill.call_args.args[0]
    assert isinstance(called_Bill, Bill)
    assert called_Bill.nombre == test_nombre
    assert called_Bill.telefono == test_telefono