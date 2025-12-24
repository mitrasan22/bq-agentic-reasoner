import hashlib
from typing import Dict


class LLMCache:
    """
    Very simple in-memory cache.
    Safe for Cloud Functions cold starts.
    """

    def __init__(self):
        self._cache: Dict[str, str] = {}

    def _key(self, prompt: str) -> str:
        return hashlib.sha256(prompt.encode()).hexdigest()

    def get(self, prompt: str) -> str | None:
        return self._cache.get(self._key(prompt))

    def set(self, prompt: str, value: str) -> None:
        self._cache[self._key(prompt)] = value
