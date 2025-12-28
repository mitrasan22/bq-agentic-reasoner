from bq_agentic_reasoner.models.public import RunResult
from bq_agentic_reasoner.llm.explainer import LLMExplainer
from bq_agentic_reasoner.rewrite.candidate_generator import CandidateGenerator
from bq_agentic_reasoner.rewrite.ranker import RewriteRanker
from bq_agentic_reasoner.agents.query_optimization_agent import QueryOptimizationAgent
import logging

class EnrichmentPipeline:
    """
    Executes slow, async enrichment:
    - LLM explanation
    - Query rewrite generation
    - Candidate ranking

    Cloud Functions safe (lazy initialization).
    """

    def __init__(self):
        self._llm = None
        self._generator = None
        self._ranker = None
        self._optimizer = None

    # ---------- lazy getters ----------

    def _get_llm(self) -> LLMExplainer:
        if self._llm is None:
            self._llm = LLMExplainer()
        return self._llm

    def _get_generator(self) -> CandidateGenerator:
        if self._generator is None:
            self._generator = CandidateGenerator()
        return self._generator

    def _get_ranker(self) -> RewriteRanker:
        if self._ranker is None:
            self._ranker = RewriteRanker()
        return self._ranker

    def _get_optimizer(self) -> QueryOptimizationAgent:
        if self._optimizer is None:
            self._optimizer = QueryOptimizationAgent(
                self._get_generator()
            )
        return self._optimizer

    # ---------- public API ----------

    def run(self, event: dict, realtime_result) -> RunResult:
        llm = self._get_llm()
        recommendation = llm.generate(realtime_result)
        logging.info(f"LLM Recommendation: {recommendation}")    

        rewrite_set = None
        if event.get("query"):
            optimizer = self._get_optimizer()
            ranker = self._get_ranker()

            candidates = optimizer.run(
                sql=event["query"],
                metadata=event["metadata"],
            )

            rewrite_set = ranker.rank(
                original_sql=event["query"],
                candidates=candidates,
            )
        result_data = realtime_result.dict()
        result_data.pop("status", None)
        return RunResult(
            **result_data,
            recommendation=recommendation,
            rewrite_set=rewrite_set,
            status="ENRICHED",
        )
