import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from app.core.domain.entities.healthcheck_entity import HealthStatus
from app.infrastructure.api.main import app

@pytest.mark.asyncio
async def test_healthcheck_success():
    with patch(
        'app.core.application.factories.healthcheck_factory.HealthCheckFactory.create'
    ) as mock_factory:
        # Configurar el mock del context manager asincrónico
        mock_service = AsyncMock()
        mock_service.check_health.return_value = HealthStatus(
            status="OK",
            timestamp=datetime(2023, 1, 1, 12, 0, 0),  # Timestamp fijo
            details={
                "database": {
                    "status": "connected",
                    "error_type": None,
                    "provider": "postgres"
                }
            }
        )
        
        # Mockear el comportamiento del async with
        mock_factory.return_value = AsyncMock(
            __aenter__=AsyncMock(return_value=mock_service),
            __aexit__=AsyncMock(return_value=None)
        )
        
        Users = TestClient(app)
        response = Users.get("/health")
        
        assert response.status_code == 200
        assert response.json() == {
            "status": "OK",
            "timestamp": "2023-01-01T12:00:00",
            "components": {
                "database": {
                    "status": "connected",
                    "error_type": None,
                    "provider": "postgres"
                }
            }
        }

@pytest.mark.asyncio
async def test_healthcheck_failure():
    with patch('app.core.application.factories.healthcheck_factory.HealthCheckFactory.create') as mock_factory:
        mock_factory.side_effect = Exception("DB Connection failed")
        
        Users = TestClient(app)
        response = Users.get("/health")
        
        assert response.status_code == 503
        assert "Service unavailable" in response.json()["detail"]