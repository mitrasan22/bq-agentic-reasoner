from bq_agentic_reasoner.models.rewrite_feedback import RewriteFeedback
from bq_agentic_reasoner.utils.sql_fingerprint import fingerprint_sql


class RewriteFeedbackHandler:
    """
    Converts user feedback into learning-safe signals.
    """

    def process(
        self,
        *,
        original_sql: str,
        optimization_type: str,
        accepted: bool,
        confidence: str,
        user_id: str | None = None,
    ) -> RewriteFeedback:
        return RewriteFeedback(
            fingerprint=fingerprint_sql(original_sql),
            optimization_type=optimization_type,
            accepted=accepted,
            confidence=confidence,
            timestamp=None,
            user_id=user_id,
        )
