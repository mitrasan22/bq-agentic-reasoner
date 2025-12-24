from pydantic import BaseModel
from typing import List, Literal

from bq_agentic_reasoner.models.cost import CostComparison
from bq_agentic_reasoner.models.confidence import RewriteConfidence


class RewriteCandidate(BaseModel):
    """
    One optimized query candidate.
    """

    optimized_query: str

    optimizations_applied: List[
        Literal[
            "PARTITION_FILTER",
            "SELECT_PRUNING",
            "JOIN_REORDER",
            "PREDICATE_PUSHDOWN",
            "BQML_OPTIMIZATION",
            "OTHER",
        ]
    ]

    explanation: str

    cost_comparison: CostComparison
    confidence: RewriteConfidence


class RewriteSet(BaseModel):
    """
    Ranked set of rewrite candidates.
    """

    original_query: str
    candidates: List[RewriteCandidate]
