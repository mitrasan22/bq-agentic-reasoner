import re
from bq_agentic_reasoner.agents.base import BaseAgent


class RiskAgent(BaseAgent):
    """
    Detects potential governance / PII risk from SQL text.
    """

    _patterns = [
        r"\bemail\b",
        r"\bphone\b",
        r"\bssn\b",
        r"\bpan\b",
        r"\bcredit\b",
        r"\bcard\b",
    ]

    def __init__(self):
        super().__init__(name="risk_agent")

    def run(self, sql: str | None) -> str:
        if not sql:
            return "LOW"

        s = sql.lower()
        for pattern in self._patterns:
            if re.search(pattern, s):
                return "HIGH"

        return "LOW"
