import pytest
from unittest.mock import AsyncMock, patch
from app.core.application.factories.healthcheck_factory import HealthCheckFactory
from app.infrastructure.adapters.healthcheck_adapter import HealthCheckAdapter

def async_generator_main(iterable):
    async def async_generator():
        for item in iterable:
            yield item
    return async_generator()

@pytest.mark.asyncio
async def test_factory_creation():
    async with HealthCheckFactory.create() as adapter:
        assert adapter is not None
        assert hasattr(adapter, 'check_health')

@pytest.mark.asyncio
async def test_factory_session_management():
    mock_session = AsyncMock()
    mock_session.commit = AsyncMock()
    mock_session.rollback = AsyncMock()
    mock_session.close = AsyncMock()

    with patch(
        'app.core.application.factories.healthcheck_factory.get_db',
        return_value=async_generator_main([mock_session])
    ):
        async with HealthCheckFactory.create() as adapter:
            assert isinstance(adapter, HealthCheckAdapter)

        mock_session.commit.assert_awaited_once()
        mock_session.rollback.assert_not_awaited()
        mock_session.close.assert_awaited_once()

# Test para verificar rollback en caso de error
@pytest.mark.asyncio
async def test_healthcheck_factory_error_handling():
    mock_session = AsyncMock()
    mock_session.commit = AsyncMock()
    mock_session.rollback = AsyncMock()
    mock_session.close = AsyncMock()
    
    async def mock_get_db():
        yield mock_session
    
    with patch("app.core.application.factories.healthcheck_factory.get_db", new=mock_get_db):
        with patch("app.core.application.factories.healthcheck_factory.HealthCheckRepository") as mock_repo, \
             patch("app.core.application.factories.healthcheck_factory.HealthCheckAdapter") as mock_adapter:
            
            mock_adapter.side_effect = Exception("Test error")
            
            with pytest.raises(Exception) as exc_info:
                async with HealthCheckFactory.create():
                    pass
                    
            # Verificar rollback y cierre
            assert str(exc_info.value) == "Test error"
            mock_session.rollback.assert_awaited_once()
            mock_session.close.assert_awaited_once()
            mock_session.commit.assert_not_awaited()