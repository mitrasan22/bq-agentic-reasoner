import re


class BigQuerySandboxGuard:
    """
    Prevents dangerous BigQuery operations.
    """

    _blocked_patterns = [
        r"(?i)\binsert\b",
        r"(?i)\bupdate\b",
        r"(?i)\bdelete\b",
        r"(?i)\bmerge\b",
        r"(?i)\bdrop\b",
        r"(?i)\bcreate\s+table\b",
    ]

    def validate_sql(self, sql: str) -> bool:
        """
        Ensure SQL is read-only and safe.
        """

        if not sql:
            return False

        for pattern in self._blocked_patterns:
            if re.search(pattern, sql):
                return False

        return True
