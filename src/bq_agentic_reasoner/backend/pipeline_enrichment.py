from bq_agentic_reasoner.models.public import RunResult
from bq_agentic_reasoner.llm.explainer import LLMExplainer
from bq_agentic_reasoner.rewrite.candidate_generator import CandidateGenerator
from bq_agentic_reasoner.rewrite.ranker import RewriteRanker
from bq_agentic_reasoner.agents.query_optimization_agent import QueryOptimizationAgent


class EnrichmentPipeline:
    """
    Executes slow, async enrichment:
    - LLM explanation
    - Query rewrite generation
    - Candidate ranking
    """

    def __init__(self):
        self.llm = LLMExplainer()
        self.generator = CandidateGenerator()
        self.ranker = RewriteRanker()
        self.optimizer = QueryOptimizationAgent(self.generator)

    def run(self, event: dict, realtime_result) -> RunResult:
        recommendation = self.llm.generate(realtime_result)

        rewrite_set = None
        if event.get("query"):
            candidates = self.optimizer.run(
                sql=event["query"],
                metadata=event["metadata"],
            )

            rewrite_set = self.ranker.rank(
                original_sql=event["query"],
                candidates=candidates,
            )

        return RunResult(
            **realtime_result.dict(),
            recommendation=recommendation,
            rewrite_set=rewrite_set,
            status="ENRICHED",
        )
