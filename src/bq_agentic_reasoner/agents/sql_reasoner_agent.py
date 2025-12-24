import re
from bq_agentic_reasoner.agents.base import BaseAgent


class SQLIntentAgent(BaseAgent):
    """
    Infers high-level intent from SQL text.
    """

    def __init__(self):
        super().__init__(name="sql_intent_agent")

    def run(self, sql: str | None) -> str:
        if not sql:
            return "UNKNOWN"

        s = sql.lower()

        if re.search(r"\bcreate\s+model\b", s):
            return "BQML_TRAINING"

        if re.search(r"\bml\.predict\b", s):
            return "BQML_PREDICT"

        if " join " in s:
            return "JOIN_QUERY"

        if " group by " in s:
            return "AGGREGATION"

        if re.search(r"select\s+\*", s):
            return "SELECT_STAR"

        return "SIMPLE_SELECT"
