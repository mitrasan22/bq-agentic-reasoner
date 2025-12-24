import re


class PIIScrubber:
    """
    Removes potential PII from text.
    """

    _patterns = [
        r"\b\d{12}\b",                # Aadhaar-like
        r"\b\d{16}\b",                # Credit card-like
        r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",  # Email
        r"\b\d{10}\b",                # Phone
    ]

    def scrub(self, text: str | None) -> str | None:
        if not text:
            return None

        for pattern in self._patterns:
            text = re.sub(pattern, "<REDACTED>", text)

        return text
