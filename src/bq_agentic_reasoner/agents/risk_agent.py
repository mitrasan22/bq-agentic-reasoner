import re
from bq_agentic_reasoner.agents.base import BaseAgent

class RiskAgent(BaseAgent):
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

    def run(self, sql: str | None, slots: int = 0) -> str:
        if not sql:
            return "LOW"

        # 1. Check for Heavy Resource Usage (Slots)
        # 3,600,000 ms = 1 hour of slot usage
        if slots > 3600000:
            return "HIGH"

        # 2. Check for PII Risk
        s = sql.lower()
        for pattern in self._patterns:
            if re.search(pattern, s):
                return "HIGH"

        return "LOW"