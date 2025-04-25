import pytest
from unittest.mock import AsyncMock
from sqlalchemy.exc import OperationalError, DatabaseError, SQLAlchemyError
from app.infrastructure.database.repositories.healthcheck_repository import HealthCheckRepository

@pytest.mark.asyncio
async def test_check_db_health_success():
    mock_session = AsyncMock()
    repository = HealthCheckRepository(mock_session)
    
    result = await repository.check_db_health()
    
    assert result["status"] is True
    assert result["error"] is None
    mock_session.execute.assert_awaited_once()

@pytest.mark.asyncio
async def test_check_db_health_operational_error():
    mock_session = AsyncMock()
    mock_session.execute.side_effect = OperationalError("", "", "Connection failed")
    repository = HealthCheckRepository(mock_session)
    
    result = await repository.check_db_health()
    
    assert result["status"] is False
    assert result["error"] == "connection_failed"

@pytest.mark.asyncio
async def test_check_db_health_general_error():
    mock_session = AsyncMock()
    mock_session.execute.side_effect = Exception("Unexpected error")
    repository = HealthCheckRepository(mock_session)
    
    result = await repository.check_db_health()
    
    assert result["status"] is False
    assert result["error"] == "unexpected_error"

@pytest.mark.asyncio
async def test_check_db_health_database_error():
    mock_session = AsyncMock()
    mock_session.execute.side_effect = DatabaseError("Query failed", None, None)
    repository = HealthCheckRepository(mock_session)
    
    result = await repository.check_db_health()
    
    assert result["status"] is False
    assert result["error"] == "query_failed"

@pytest.mark.asyncio
async def test_check_db_health_sqlalchemy_error():
    mock_session = AsyncMock()
    mock_session.execute.side_effect = SQLAlchemyError("General DB error")
    repository = HealthCheckRepository(mock_session)
    
    result = await repository.check_db_health()
    
    assert result["status"] is False
    assert result["error"] == "database_error"