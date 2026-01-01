from bq_agentic_reasoner.llm.hf_client import HuggingFaceClient
from bq_agentic_reasoner.llm.prompt_builder import PromptBuilder
from bq_agentic_reasoner.llm.sql_validator import LLMOutputValidator
from bq_agentic_reasoner.llm.cache import LLMCache
from bq_agentic_reasoner.models.public import (
    RealtimeResult,
    LLMRecommendation,
)
from bq_agentic_reasoner.security.validator import SecurityValidator
class LLMExplainer:
    """
    Agentic LLM orchestrator.
    Cloud Functions safe (lazy init).
    """
    def __init__(self):
        self._client = None
        self._builder = None
        self._validator = None
        self._cache = None
        self.security_validator = SecurityValidator()

    def _get_client(self) -> HuggingFaceClient:
        if self._client is None:
            self._client = HuggingFaceClient()
        return self._client

    def _get_builder(self) -> PromptBuilder:
        if self._builder is None:
            self._builder = PromptBuilder()
        return self._builder

    def _get_validator(self) -> LLMOutputValidator:
        if self._validator is None:
            self._validator = LLMOutputValidator()
        return self._validator

    def _get_cache(self) -> LLMCache:
        if self._cache is None:
            self._cache = LLMCache()
        return self._cache

    def generate(
        self,
        result: RealtimeResult,
        sql: str | None = None,
    ) -> LLMRecommendation | None:

        builder = self._get_builder()
        cache = self._get_cache()
        validator = self._get_validator()
        client = self._get_client()

        # Added security call
        safe_sql = self.security_validator.secure_sql_for_llm(sql)

        prompt = builder.build_explanation_prompt(
            result=result,
            sql=safe_sql,
        )

        cached = cache.get(prompt)
        if cached:
            text = cached
        else:
            text = client.generate(prompt)
            cache.set(prompt, text)

        # Added security call
        text = self.security_validator.secure_text_output(text)

        if not text or not validator.validate(text):
            return None

        return LLMRecommendation(
            title="LLM Analysis & Recommendation",
            rationale=text[:1000],
            confidence="MEDIUM",
            category="COST_OPTIMIZATION",
        )
