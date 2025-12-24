from typing import List
from bq_agentic_reasoner.models.rewrite import RewriteCandidate
from bq_agentic_reasoner.models.confidence import RewriteConfidence
from bq_agentic_reasoner.rewrite.validator import SQLValidator
from bq_agentic_reasoner.rewrite.comparator import CostComparator


class CandidateGenerator:
    """
    Generates optimization candidates for SQL queries.
    """

    def __init__(self):
        self.validator = SQLValidator()
        self.cost_comparator = CostComparator()

    def generate(self, *, sql: str, metadata: dict) -> List[RewriteCandidate]:
        candidates: List[RewriteCandidate] = []

        base_cost_gb = metadata.get("estimated_bytes", 0) / (1024 ** 3)

        # ---- Rule 1: SELECT * pruning ----
        if "select *" in sql.lower():
            optimized = sql.replace("*", "<explicit_columns>")

            if self.validator.validate(optimized):
                cost = self.cost_comparator.estimate(
                    original_gb=base_cost_gb,
                    optimized_gb=base_cost_gb * 0.6,
                )

                candidates.append(
                    RewriteCandidate(
                        optimized_query=optimized,
                        optimizations_applied=["SELECT_PRUNING"],
                        explanation="Replaced SELECT * with explicit columns to reduce scanned data.",
                        cost_comparison=cost,
                        confidence=RewriteConfidence(
                            score=0.7,
                            level="MEDIUM",
                            reasons=["Common BigQuery optimization"],
                        ),
                    )
                )

        # ---- Rule 2: Partition filter hint ----
        if "where" not in sql.lower():
            optimized = sql + "\nWHERE <partition_column> >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)"

            if self.validator.validate(optimized):
                cost = self.cost_comparator.estimate(
                    original_gb=base_cost_gb,
                    optimized_gb=base_cost_gb * 0.4,
                )

                candidates.append(
                    RewriteCandidate(
                        optimized_query=optimized,
                        optimizations_applied=["PARTITION_FILTER"],
                        explanation="Added partition filter to limit scanned partitions.",
                        cost_comparison=cost,
                        confidence=RewriteConfidence(
                            score=0.8,
                            level="HIGH",
                            reasons=["Partition pruning significantly reduces scan cost"],
                        ),
                    )
                )

        return candidates
