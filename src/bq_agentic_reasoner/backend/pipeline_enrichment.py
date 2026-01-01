from bq_agentic_reasoner.models.public import RunResult
from bq_agentic_reasoner.llm.explainer import LLMExplainer
from bq_agentic_reasoner.rewrite.candidate_generator import CandidateGenerator
from bq_agentic_reasoner.rewrite.ranker import RewriteRanker
from bq_agentic_reasoner.agents.query_optimization_agent import QueryOptimizationAgent
from bq_agentic_reasoner.agents.bqml_optimization_agent import BQMLOptimizationAgent
from bq_agentic_reasoner.bigquery.bqml_client import BQMLMetadataClient
from bq_agentic_reasoner.bigquery.sandbox_guard import BigQuerySandboxGuard
from bq_agentic_reasoner.security.validator import SecurityValidator
import logging

class EnrichmentPipeline:
    def __init__(self):
        self._llm = None
        self._generator = None
        self._ranker = None
        self._optimizer = None
        self._bqml_optimizer = None
        self._bqml_client = None
        self._guard = BigQuerySandboxGuard()
        self.security = SecurityValidator()

    def _get_llm(self):
        if not self._llm: self._llm = LLMExplainer()
        return self._llm

    def _get_generator(self):
        if not self._generator: self._generator = CandidateGenerator()
        return self._generator

    def _get_ranker(self):
        if not self._ranker: self._ranker = RewriteRanker()
        return self._ranker

    def _get_optimizer(self):
        if not self._optimizer: 
            self._optimizer = QueryOptimizationAgent(self._get_generator())
        return self._optimizer

    def _get_bqml_optimizer(self):
        if not self._bqml_optimizer:
            self._bqml_optimizer = BQMLOptimizationAgent(self._get_generator())
        return self._bqml_optimizer
    
    def _get_bqml_client(self):
        if not self._bqml_client: self._bqml_client = BQMLMetadataClient()
        return self._bqml_client

    def run(self, event: dict, realtime_result) -> RunResult:
        raw_query = event.get("query")
        ml_stats = None
        
        if event.get("job_type") == "BQML":
            model_fqn = event.get("metadata", {}).get("model_fqn")
            if model_fqn:
                try:
                    ml_stats = self._get_bqml_client().get_model_evaluation(model_fqn)
                except Exception as e:
                    logging.warning(f"Could not fetch ML stats for {model_fqn}: {e}")

        # Clean query before passing to LLM
        safe_query = self.security.secure_sql_for_llm(raw_query)
        logging.info(f"ML STATS: {ml_stats}")
        recommendation = self._get_llm().generate(
            result=realtime_result, 
            sql=safe_query,
            ml_context=ml_stats
        )

        rewrite_set = None
        if raw_query:
            agent = self._get_bqml_optimizer() if event.get("job_type") == "BQML" else self._get_optimizer()
            candidates = agent.run(sql=raw_query, metadata=event.get("metadata", {}), ml_context=ml_stats)
            safe_candidates = [c for c in candidates if self._guard.validate_sql(c.sql)]
            
            rewrite_set = self._get_ranker().rank(
                original_sql=raw_query,
                candidates=safe_candidates
            )

        result_data = realtime_result.dict()
        result_data.pop("status", None)
        
        return RunResult(
            **result_data,
            recommendation=recommendation,
            rewrite_set=rewrite_set,
            status="ENRICHED",
        )