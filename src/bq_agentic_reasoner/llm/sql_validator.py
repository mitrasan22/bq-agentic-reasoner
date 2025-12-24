import re
from bq_agentic_reasoner.config import load_config


class LLMOutputValidator:
    """
    Validates LLM output before exposing to users.
    """

    def __init__(self):
        config = load_config()
        self.blocked = config["security"].get("blocked_sql_patterns", [])

    def validate(self, text: str) -> bool:
        if not text:
            return False

        for pattern in self.blocked:
            if re.search(pattern, text):
                return False

        return True
