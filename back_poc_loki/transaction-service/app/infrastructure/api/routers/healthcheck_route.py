import logging
from fastapi import APIRouter, HTTPException
from app.core.application.factories.healthcheck_factory import (
    HealthCheckFactory
)
from app.infrastructure.api.schemas.healthcheck_schema import (
    HealthCheckResponse
)
from app.core.domain.entities.healthcheck_entity import HealthStatus

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    try:
        async with HealthCheckFactory.create() as healthcheck_service:
            health_status: HealthStatus = await (
                healthcheck_service.check_health()
            )

            return {
                "status": health_status.status,
                "timestamp": health_status.timestamp.isoformat(),
                "components": health_status.details
            }

    except Exception as e:
        logger.error(f"Healthcheck critical failure: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=503,
            detail="Service unavailable"
        ) from e
