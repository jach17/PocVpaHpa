from abc import ABC, abstractmethod
from app.core.domain.entities.healthcheck_entity import HealthStatus

class HealthCheckPort(ABC):
    @abstractmethod
    async def check_health(self) -> HealthStatus:
        raise NotImplementedError