from bq_agentic_reasoner.security.sanitizer import SQLSanitizer
from bq_agentic_reasoner.security.redactor import SQLRedactor
from bq_agentic_reasoner.security.prompt_firewall import PromptFirewall
from bq_agentic_reasoner.security.pii_scrubber import PIIScrubber


class SecurityValidator:
    """
    Composite security validator.
    """

    def __init__(self):
        self.sanitizer = SQLSanitizer()
        self.redactor = SQLRedactor()
        self.firewall = PromptFirewall()
        self.scrubber = PIIScrubber()

    def secure_sql_for_llm(self, sql: str | None) -> str | None:
        sql = self.sanitizer.sanitize(sql)
        sql = self.redactor.redact(sql)
        return sql

    def secure_text_output(self, text: str | None) -> str | None:
        if not self.firewall.is_safe(text):
            return None
        return self.scrubber.scrub(text)
