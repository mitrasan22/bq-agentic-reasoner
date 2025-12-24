from pydantic import BaseModel
from typing import Literal, List


class RewriteConfidence(BaseModel):
    """
    Confidence score for an optimized query.
    """

    score: float  # 0.0 – 1.0

    level: Literal["LOW", "MEDIUM", "HIGH"]

    reasons: List[str]
