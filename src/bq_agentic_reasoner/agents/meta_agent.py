from bq_agentic_reasoner.agents.base import BaseAgent


class SeverityAgent(BaseAgent):
    """
    Aggregates cost, risk, and intent into a severity level.
    """

    def __init__(self):
        super().__init__(name="severity_agent")

    def run(self, *, cost_gb: float, risk: str, intent: str) -> str:
        score = 0

        # Cost contribution
        if cost_gb > 10:
            score += 2
        elif cost_gb > 5:
            score += 1

        # Risk contribution
        if risk == "HIGH":
            score += 2

        # Intent contribution
        if intent in {"JOIN_QUERY", "AGGREGATION"}:
            score += 1

        if score >= 4:
            return "CRITICAL"
        if score >= 3:
            return "HIGH"
        if score >= 2:
            return "MEDIUM"
        return "LOW"
