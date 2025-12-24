import re
from bq_agentic_reasoner.config import load_config


class SQLValidator:
    """
    Enforces safety rules on rewritten SQL.
    """

    def __init__(self):
        config = load_config()
        self.max_len = config["security"].get("max_sql_length", 20000)
        self.blocked = config["security"].get("blocked_sql_patterns", [])

    def validate(self, sql: str) -> bool:
        if not sql or len(sql) > self.max_len:
            return False

        for pattern in self.blocked:
            if re.search(pattern, sql):
                return False

        return True
