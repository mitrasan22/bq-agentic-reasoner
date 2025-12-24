from typing import TypedDict, Optional, Dict, Any
from datetime import datetime


class RunDocument(TypedDict):
    """
    Firestore schema for a single run.
    """

    job_id: str
    timestamp: datetime
    job_type: str

    severity: str
    intent: str
    estimated_cost_gb: float
    risk: str

    session_id: Optional[str]
    status: str

    recommendation: Optional[Dict[str, Any]]
    rewrite_set: Optional[Dict[str, Any]]

    created_at: datetime


class RewriteFeedbackDocument(TypedDict):
    """
    Firestore schema for rewrite feedback.
    """

    fingerprint: str
    optimization_type: str

    accepted: bool
    confidence: str

    user_id: Optional[str]
    timestamp: datetime
