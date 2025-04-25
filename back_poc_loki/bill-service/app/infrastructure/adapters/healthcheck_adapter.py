from datetime import datetime
from app.core.application.ports.services.healthcheck_port import (
    HealthCheckPort
)
from app.core.domain.entities.healthcheck_entity import HealthStatus
from app.infrastructure.database.repositories.healthcheck_repository import (
    HealthCheckRepository
)


class HealthCheckAdapter(HealthCheckPort):
    def __init__(self, repository: HealthCheckRepository):
        self.repository = repository

    async def check_health(self) -> HealthStatus:
        db_result = await self.repository.check_db_health()

        status = "OK" if db_result["status"] else "ERROR"
        details = {
            "database": {
                "status": "connected" if db_result["status"] else "disconnected",
                "error_type": db_result["error"],
                "provider": "postgres"
            }
        }

        return HealthStatus(
            status=status,
            timestamp=datetime.now(),
            details=details
        )
