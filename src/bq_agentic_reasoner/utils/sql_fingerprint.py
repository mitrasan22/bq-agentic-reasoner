import re
from bq_agentic_reasoner.utils.hashing import sha256_hash


_KEYWORDS = [
    "select",
    "from",
    "where",
    "group by",
    "order by",
    "join",
    "inner join",
    "left join",
    "right join",
    "full join",
    "having",
    "limit",
]


def normalize_sql(sql: str) -> str:
    """
    Normalize SQL to structure-only representation.
    """

    sql = sql.lower()

    # Remove literals
    sql = re.sub(r"'[^']*'", "?", sql)
    sql = re.sub(r'"[^"]*"', "?", sql)
    sql = re.sub(r"\b\d+(\.\d+)?\b", "?", sql)

    # Remove identifiers
    sql = re.sub(r"`[^`]+`", "<id>", sql)
    sql = re.sub(r"\b[a-zA-Z_][a-zA-Z0-9_]*\b", "<id>", sql)

    # Keep keywords
    for kw in _KEYWORDS:
        sql = sql.replace(f"<id> {kw} <id>", kw)

    # Normalize whitespace
    sql = re.sub(r"\s+", " ", sql).strip()

    return sql


def fingerprint_sql(sql: str) -> str:
    """
    Generate a privacy-safe fingerprint of SQL structure.
    """
    if not sql:
        return ""

    normalized = normalize_sql(sql)
    return sha256_hash(normalized)
