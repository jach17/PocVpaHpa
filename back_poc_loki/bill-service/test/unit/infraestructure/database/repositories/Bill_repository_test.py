import pytest
from sqlalchemy import select
from unittest.mock import MagicMock
from unittest.mock import AsyncMock
from sqlalchemy.exc import SQLAlchemyError
from app.core.domain.entities.BillRepository.Bill import Bill
from app.infrastructure.database.repositories.Bill_repository import BillRepository
from app.infrastructure.database.models.Bill_model import BillModel

@pytest.mark.asyncio
async def test_get_all_Bills_success():
    mock_Bill1 = MagicMock(spec=BillModel, id=1, nombre="John", telefono="123")
    mock_Bill2 = MagicMock(spec=BillModel, id=2, nombre="Jane", telefono="456")
    
    mock_session = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [mock_Bill1, mock_Bill2]
    mock_session.execute.return_value = mock_result
    
    repo = BillRepository(mock_session)
    result = await repo.get_all_Bills()
    
    assert len(result) == 2
    assert result[0].nombre == "John"

    mock_session.execute.assert_awaited_once()
    args, _ = mock_session.execute.call_args
    assert isinstance(args[0], select(BillModel).__class__)

@pytest.mark.asyncio
async def test_get_all_Bills_error():
    mock_session = AsyncMock()
    mock_session.execute.side_effect = SQLAlchemyError("DB error")
    
    repo = BillRepository(mock_session)
    with pytest.raises(RuntimeError) as exc_info:
        await repo.get_all_Bills()
    
    assert "DB error" in str(exc_info.value)

@pytest.mark.asyncio
async def test_get_Bill_by_id_found():
    mock_Bill = AsyncMock(id=1, nombre="John", telefono="123")
    mock_session = AsyncMock()
    mock_session.get.return_value = mock_Bill

    repo = BillRepository(mock_session)
    result = await repo.get_Bill_by_id(1)

    assert result.id == 1
    assert result.nombre == "John"
    mock_session.get.assert_awaited_once_with(BillModel, 1)

@pytest.mark.asyncio
async def test_get_Bill_by_id_not_found():
    mock_session = AsyncMock()
    mock_session.get.return_value = None
    
    repo = BillRepository(mock_session)
    result = await repo.get_Bill_by_id(999)
    
    assert result is None

@pytest.mark.asyncio
async def test_create_Bill_success():
    mock_session = AsyncMock()
    test_Bill = Bill(id=None, nombre="New", telefono="999")

    repo = BillRepository(mock_session)
    result = await repo.create_Bill(test_Bill)

    assert isinstance(result, Bill)
    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()
    assert result.nombre == "New"

@pytest.mark.asyncio
async def test_update_Bill_success():
    mock_Bill = AsyncMock(id=1, nombre="Old", telefono="111")
    mock_session = AsyncMock()
    mock_session.get.return_value = mock_Bill

    repo = BillRepository(mock_session)
    result = await repo.update_Bill("1", "New", "999")

    assert result == mock_Bill
    assert mock_Bill.nombre == "New"
    assert mock_Bill.telefono == "999"
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once_with(mock_Bill)

@pytest.mark.asyncio
async def test_update_Bill_not_found():
    mock_session = AsyncMock()
    mock_session.get.return_value = None
    
    repo = BillRepository(mock_session)
    result = await repo.update_Bill("999", "Name", "000")
    
    assert result is None
    mock_session.commit.assert_not_awaited()

@pytest.mark.asyncio
async def test_update_Bill_error():
    mock_session = AsyncMock()
    mock_session.get.side_effect = SQLAlchemyError("Update error")
    
    repo = BillRepository(mock_session)
    with pytest.raises(RuntimeError) as exc_info:
        await repo.update_Bill("1", "New", "999")
    
    assert "DB error" in str(exc_info.value)