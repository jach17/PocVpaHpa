from pydantic import BaseModel
from typing import Dict, Optional

class HealthCheckResponse(BaseModel):
    status: str
    timestamp: str
    components: Dict[str, Dict[str, Optional[str]]]