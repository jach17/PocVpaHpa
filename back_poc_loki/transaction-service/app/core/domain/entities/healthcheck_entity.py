from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict


class HealthStatus(BaseModel):
    status: str
    timestamp: datetime
    details: Dict[str, Dict[str, Optional[str]]]
