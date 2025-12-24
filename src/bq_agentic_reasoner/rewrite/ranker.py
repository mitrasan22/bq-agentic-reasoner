from bq_agentic_reasoner.models.rewrite import RewriteSet, RewriteCandidate


class RewriteRanker:
    """
    Ranks rewrite candidates based on estimated savings and confidence.
    """

    def rank(
        self,
        *,
        original_sql: str,
        candidates: list[RewriteCandidate],
    ) -> RewriteSet | None:
        if not candidates:
            return None

        ranked = sorted(
            candidates,
            key=lambda c: (
                c.cost_comparison.estimated_savings_pct,
                c.confidence.score,
            ),
            reverse=True,
        )

        return RewriteSet(
            original_query=original_sql,
            candidates=ranked,
        )
