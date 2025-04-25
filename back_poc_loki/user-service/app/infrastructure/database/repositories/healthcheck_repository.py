from sqlalchemy.exc import SQLAlchemyError, OperationalError, DatabaseError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import logging

logger = logging.getLogger(__name__)

class HealthCheckRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def check_db_health(self) -> dict:
        try:
            await self.session.execute(text("SELECT 1"))
            return {"status": True, "error": None}
            
        except OperationalError as e:
            logger.error(f"Database connection error: {str(e)}")
            return {"status": False, "error": "connection_failed"}
            
        except DatabaseError as e:
            logger.error(f"Database query error: {str(e)}")
            return {"status": False, "error": "query_failed"}
            
        except SQLAlchemyError as e:
            logger.error(f"General database error: {str(e)}")
            return {"status": False, "error": "database_error"}
            
        except Exception as e:
            logger.critical(f"Unexpected error: {str(e)}")
            return {"status": False, "error": "unexpected_error"}