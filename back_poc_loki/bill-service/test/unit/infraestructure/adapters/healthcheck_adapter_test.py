import pytest
from datetime import datetime
from unittest.mock import AsyncMock
from app.core.domain.entities.healthcheck_entity import HealthStatus
from app.infrastructure.adapters.healthcheck_adapter import HealthCheckAdapter

@pytest.mark.asyncio
async def test_check_health_success():
    mock_repo = AsyncMock()
    mock_repo.check_db_health.return_value = {
        "status": True,
        "error": None
    }
    
    adapter = HealthCheckAdapter(mock_repo)
    result = await adapter.check_health()
    
    assert isinstance(result, HealthStatus)
    assert result.status == "OK"
    assert "database" in result.details

@pytest.mark.asyncio
async def test_check_health_database_failure():
    mock_repo = AsyncMock()
    mock_repo.check_db_health.return_value = {
        "status": False,
        "error": "connection_failed"
    }
    
    adapter = HealthCheckAdapter(mock_repo)
    result = await adapter.check_health()
    
    assert result.status == "ERROR"
    assert result.details["database"]["error_type"] == "connection_failed"