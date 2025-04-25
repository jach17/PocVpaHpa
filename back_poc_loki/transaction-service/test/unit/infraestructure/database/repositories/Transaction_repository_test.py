import pytest
from sqlalchemy import select
from unittest.mock import MagicMock
from unittest.mock import AsyncMock
from sqlalchemy.exc import SQLAlchemyError
from app.core.domain.entities.TransactionRepository.Transaction import Transaction
from app.infrastructure.database.repositories.Transaction_repository import TransactionRepository
from app.infrastructure.database.models.Transaction_model import TransactionModel

@pytest.mark.asyncio
async def test_get_all_Transactions_success():
    mock_Transaction1 = MagicMock(spec=TransactionModel, id=1, nombre="John", telefono="123")
    mock_Transaction2 = MagicMock(spec=TransactionModel, id=2, nombre="Jane", telefono="456")
    
    mock_session = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [mock_Transaction1, mock_Transaction2]
    mock_session.execute.return_value = mock_result
    
    repo = TransactionRepository(mock_session)
    result = await repo.get_all_Transactions()
    
    assert len(result) == 2
    assert result[0].nombre == "John"

    mock_session.execute.assert_awaited_once()
    args, _ = mock_session.execute.call_args
    assert isinstance(args[0], select(TransactionModel).__class__)

@pytest.mark.asyncio
async def test_get_all_Transactions_error():
    mock_session = AsyncMock()
    mock_session.execute.side_effect = SQLAlchemyError("DB error")
    
    repo = TransactionRepository(mock_session)
    with pytest.raises(RuntimeError) as exc_info:
        await repo.get_all_Transactions()
    
    assert "DB error" in str(exc_info.value)

@pytest.mark.asyncio
async def test_get_Transaction_by_id_found():
    mock_Transaction = AsyncMock(id=1, nombre="John", telefono="123")
    mock_session = AsyncMock()
    mock_session.get.return_value = mock_Transaction

    repo = TransactionRepository(mock_session)
    result = await repo.get_Transaction_by_id(1)

    assert result.id == 1
    assert result.nombre == "John"
    mock_session.get.assert_awaited_once_with(TransactionModel, 1)

@pytest.mark.asyncio
async def test_get_Transaction_by_id_not_found():
    mock_session = AsyncMock()
    mock_session.get.return_value = None
    
    repo = TransactionRepository(mock_session)
    result = await repo.get_Transaction_by_id(999)
    
    assert result is None

@pytest.mark.asyncio
async def test_create_Transaction_success():
    mock_session = AsyncMock()
    test_Transaction = Transaction(id=None, nombre="New", telefono="999")

    repo = TransactionRepository(mock_session)
    result = await repo.create_Transaction(test_Transaction)

    assert isinstance(result, Transaction)
    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()
    assert result.nombre == "New"

@pytest.mark.asyncio
async def test_update_Transaction_success():
    mock_Transaction = AsyncMock(id=1, nombre="Old", telefono="111")
    mock_session = AsyncMock()
    mock_session.get.return_value = mock_Transaction

    repo = TransactionRepository(mock_session)
    result = await repo.update_Transaction("1", "New", "999")

    assert result == mock_Transaction
    assert mock_Transaction.nombre == "New"
    assert mock_Transaction.telefono == "999"
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once_with(mock_Transaction)

@pytest.mark.asyncio
async def test_update_Transaction_not_found():
    mock_session = AsyncMock()
    mock_session.get.return_value = None
    
    repo = TransactionRepository(mock_session)
    result = await repo.update_Transaction("999", "Name", "000")
    
    assert result is None
    mock_session.commit.assert_not_awaited()

@pytest.mark.asyncio
async def test_update_Transaction_error():
    mock_session = AsyncMock()
    mock_session.get.side_effect = SQLAlchemyError("Update error")
    
    repo = TransactionRepository(mock_session)
    with pytest.raises(RuntimeError) as exc_info:
        await repo.update_Transaction("1", "New", "999")
    
    assert "DB error" in str(exc_info.value)