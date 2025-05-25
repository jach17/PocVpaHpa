import pytest
from sqlalchemy import select
from unittest.mock import MagicMock
from unittest.mock import AsyncMock
from sqlalchemy.exc import SQLAlchemyError
from app.core.domain.entities.UserRepository.User import User
from app.infrastructure.database.repositories.User_repository import UserRepository
from app.infrastructure.database.models.User_model import UserModel

@pytest.mark.asyncio
async def test_get_all_Users_success():
    mock_User1 = MagicMock(spec=UserModel, id=1, nombre="John", telefono="123")
    mock_User2 = MagicMock(spec=UserModel, id=2, nombre="Jane", telefono="456")
    
    mock_session = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [mock_User1, mock_User2]
    mock_session.execute.return_value = mock_result
    
    repo = UserRepository(mock_session)
    result = await repo.get_all_Users()
    
    assert len(result) == 2
    assert result[0].nombre == "John"

    mock_session.execute.assert_awaited_once()
    args, _ = mock_session.execute.call_args
    assert isinstance(args[0], select(UserModel).__class__)

@pytest.mark.asyncio
async def test_get_all_Users_error():
    mock_session = AsyncMock()
    mock_session.execute.side_effect = SQLAlchemyError("DB error")
    
    repo = UserRepository(mock_session)
    with pytest.raises(RuntimeError) as exc_info:
        await repo.get_all_Users()
    
    assert "DB error" in str(exc_info.value)

@pytest.mark.asyncio
async def test_get_User_by_id_found():
    mock_User = AsyncMock(id=1, nombre="John", telefono="123")
    mock_session = AsyncMock()
    mock_session.get.return_value = mock_User

    repo = UserRepository(mock_session)
    result = await repo.get_User_by_id(1)

    assert result.id == 1
    assert result.nombre == "John"
    mock_session.get.assert_awaited_once_with(UserModel, 1)

@pytest.mark.asyncio
async def test_get_User_by_id_not_found():
    mock_session = AsyncMock()
    mock_session.get.return_value = None
    
    repo = UserRepository(mock_session)
    result = await repo.get_User_by_id(999)
    
    assert result is None

@pytest.mark.asyncio
async def test_create_User_success():
    mock_session = AsyncMock()
    test_User = User(id=None, nombre="New", telefono="999")

    repo = UserRepository(mock_session)
    result = await repo.create_User(test_User)

    assert isinstance(result, User)
    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()
    assert result.nombre == "New"

@pytest.mark.asyncio
async def test_update_User_success():
    mock_User = AsyncMock(id=1, nombre="Old", telefono="111")
    mock_session = AsyncMock()
    mock_session.get.return_value = mock_User

    repo = UserRepository(mock_session)
    result = await repo.update_User("1", "New", "999")

    assert result == mock_User
    assert mock_User.nombre == "New"
    assert mock_User.telefono == "999"
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once_with(mock_User)

@pytest.mark.asyncio
async def test_update_User_not_found():
    mock_session = AsyncMock()
    mock_session.get.return_value = None
    
    repo = UserRepository(mock_session)
    result = await repo.update_User("999", "Name", "000")
    
    assert result is None
    mock_session.commit.assert_not_awaited()

@pytest.mark.asyncio
async def test_update_User_error():
    mock_session = AsyncMock()
    mock_session.get.side_effect = SQLAlchemyError("Update error")
    
    repo = UserRepository(mock_session)
    with pytest.raises(RuntimeError) as exc_info:
        await repo.update_User("1", "New", "999")
    
    assert "DB error" in str(exc_info.value)