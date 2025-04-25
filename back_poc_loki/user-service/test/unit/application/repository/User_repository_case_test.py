import pytest
from unittest.mock import MagicMock, create_autospec
from app.core.application.ports.services.User_repository_service_port import UserRepositoryServicePort
from app.core.domain.entities.UserRepository.User import User
from app.core.application.use_cases.repository.User_repository_case import (
    get_all_Users_case, get_User_case, update_User_case, create_User_case
)

@pytest.fixture
def mock_service():
    return create_autospec(UserRepositoryServicePort, instance=True)

@pytest.mark.asyncio
async def test_get_all_Users_case(mock_service):
    expected_result = [MagicMock(), MagicMock()]
    mock_service.get_all_Users.return_value = expected_result

    result = await get_all_Users_case(mock_service)

    assert result == expected_result
    mock_service.get_all_Users.assert_awaited_once()

@pytest.mark.asyncio
async def test_get_User_case(mock_service):
    test_id = 123
    expected_User = MagicMock()
    mock_service.get_User_by_id.return_value = expected_User

    result = await get_User_case(mock_service, test_id)

    assert result == expected_User
    mock_service.get_User_by_id.assert_awaited_once_with(test_id)

@pytest.mark.asyncio
async def test_update_User_case(mock_service):
    test_data = {
        "id": "User-123",
        "nombre": "Ana",
        "telefono": "555-9876"
    }
    mock_service.update_User.return_value = MagicMock()

    result = await update_User_case(
        mock_service,
        test_data["id"],
        test_data["nombre"],
        test_data["telefono"]
    )

    assert result is not None
    mock_service.update_User.assert_awaited_once_with(
        test_data["id"],
        test_data["nombre"],
        test_data["telefono"]
    )

@pytest.mark.asyncio
async def test_create_User_case(mock_service):
    test_nombre = "Carlos"
    test_telefono = "555-5555"

    mock_service.create_User.return_value = MagicMock()

    result = await create_User_case(mock_service, test_nombre, test_telefono)

    assert result is not None
    mock_service.create_User.assert_awaited_once()

    called_User = mock_service.create_User.call_args.args[0]
    assert isinstance(called_User, User)
    assert called_User.nombre == test_nombre
    assert called_User.telefono == test_telefono