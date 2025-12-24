import re


class SQLSanitizer:
    """
    Sanitizes raw SQL text.
    """

    _control_chars = re.compile(r"[\x00-\x08\x0B\x0C\x0E-\x1F]")

    def sanitize(self, sql: str | None) -> str | None:
        if not sql:
            return None

        # Remove control characters
        sql = self._control_chars.sub("", sql)

        # Normalize whitespace
        sql = re.sub(r"\s+", " ", sql).strip()

        return sql
