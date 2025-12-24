from bq_agentic_reasoner.models.cost import CostComparison


class CostComparator:
    """
    Estimates cost impact of query rewrite.
    Uses heuristics only — never executes SQL.
    """

    def estimate(
        self,
        *,
        original_gb: float,
        optimized_gb: float,
    ) -> CostComparison:
        if original_gb <= 0:
            savings = 0.0
        else:
            savings = max(
                0.0,
                (original_gb - optimized_gb) / original_gb * 100,
            )

        return CostComparison(
            original_estimated_gb=round(original_gb, 3),
            optimized_estimated_gb=round(optimized_gb, 3),
            estimated_savings_pct=round(savings, 2),
        )
