from bq_agentic_reasoner.llm.hf_client import HuggingFaceClient
from bq_agentic_reasoner.llm.prompt_builder import PromptBuilder
from bq_agentic_reasoner.llm.sql_validator import LLMOutputValidator
from bq_agentic_reasoner.llm.cache import LLMCache
from bq_agentic_reasoner.models.public import (
    RealtimeResult,
    LLMRecommendation,
)


class LLMExplainer:
    """
    Agentic LLM orchestrator.
    """

    def __init__(self):
        self.client = HuggingFaceClient()
        self.builder = PromptBuilder()
        self.validator = LLMOutputValidator()
        self.cache = LLMCache()

    def generate(
        self,
        result: RealtimeResult,
        sql: str | None = None,
    ) -> LLMRecommendation | None:

        prompt = self.builder.build_explanation_prompt(
            result=result,
            sql=sql,
        )

        cached = self.cache.get(prompt)
        if cached:
            text = cached
        else:
            text = self.client.generate(prompt)
            self.cache.set(prompt, text)

        if not self.validator.validate(text):
            return None
        return LLMRecommendation(
            title="LLM Analysis & Recommendation",
            rationale=text[:1000],
            confidence="MEDIUM",
            category="COST_OPTIMIZATION",
        )
