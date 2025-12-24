import re


class SQLRedactor:
    """
    Redacts project, dataset, and table identifiers.
    """

    _fqn_pattern = re.compile(
        r"`?([a-zA-Z0-9_\-]+)\.([a-zA-Z0-9_\-]+)\.([a-zA-Z0-9_\-]+)`?"
    )

    def redact(self, sql: str | None) -> str | None:
        if not sql:
            return None

        return self._fqn_pattern.sub(
            "`<project>.<dataset>.<table>`",
            sql,
        )
