from pydantic import BaseModel
from typing import Literal, Optional
from datetime import datetime


class RewriteFeedback(BaseModel):
    """
    Captures user acceptance signal for learning.
    """

    fingerprint: str                 
    optimization_type: str           

    accepted: bool
    confidence: Literal["LOW", "MEDIUM", "HIGH"]

    timestamp: datetime
    user_id: Optional[str] = None
