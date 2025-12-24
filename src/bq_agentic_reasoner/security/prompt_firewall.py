import re


class PromptFirewall:
    """
    Detects prompt-injection attempts.
    """

    _blocked_phrases = [
        r"(?i)ignore previous instructions",
        r"(?i)system prompt",
        r"(?i)you are chatgpt",
        r"(?i)act as",
        r"(?i)execute sql",
    ]

    def is_safe(self, text: str | None) -> bool:
        if not text:
            return True

        for pattern in self._blocked_phrases:
            if re.search(pattern, text):
                return False

        return True
