import hashlib


def sha256_hash(value: str) -> str:
    """
    Compute a stable SHA-256 hash.
    """
    if not value:
        return ""

    return hashlib.sha256(value.encode("utf-8")).hexdigest()
