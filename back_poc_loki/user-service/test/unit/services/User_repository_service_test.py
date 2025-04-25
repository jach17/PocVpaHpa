import pytest
from unittest.mock import MagicMock, create_autospec
from app.core.domain.services.UserRepository.User_repository_service import UserRepositoryService
from app.core.domain.entities.UserRepository.User import User
from app.core.application.ports.database.User_repository_db_port import UserRepositoryDBPort

@pytest.fixture
def mock_repo():
    return create_autospec(UserRepositoryDBPort, instance=True)

@pytest.fixture
def User_service(mock_repo):
    return UserRepositoryService(repo=mock_repo)

@pytest.mark.asyncio
async def test_get_all_Users(User_service, mock_repo):
    expected_Users = [MagicMock(), MagicMock()]
    mock_repo.get_all_Users.return_value = expected_Users

    result = await User_service.get_all_Users()
    
    assert result == expected_Users
    mock_repo.get_all_Users.assert_awaited_once()

@pytest.mark.asyncio
async def test_get_User_by_id(User_service, mock_repo):
    test_id = 123
    expected_User = MagicMock()
    mock_repo.get_User_by_id.return_value = expected_User

    result = await User_service.get_User_by_id(test_id)
    
    assert result == expected_User
    mock_repo.get_User_by_id.assert_awaited_once_with(test_id)

@pytest.mark.asyncio
async def test_update_User(User_service, mock_repo):
    test_id = "abc123"
    test_nombre = "Juan"
    test_telefono = "555-1234"
    expected_result = MagicMock()
    mock_repo.update_User.return_value = expected_result

    result = await User_service.update_User(test_id, test_nombre, test_telefono)
    
    assert result == expected_result
    mock_repo.update_User.assert_awaited_once_with(test_id, test_nombre, test_telefono)

@pytest.mark.asyncio
async def test_create_User(User_service, mock_repo):
    test_User = User(id=1, nombre="Maria", telefono="555-4321")
    expected_result = MagicMock()
    mock_repo.create_User.return_value = expected_result

    result = await User_service.create_User(test_User)
    
    assert result == expected_result
    mock_repo.create_User.assert_awaited_once_with(test_User)