from typing import List
from bq_agentic_reasoner.agents.base import BaseAgent
from bq_agentic_reasoner.rewrite.candidate_generator import CandidateGenerator
from bq_agentic_reasoner.models.rewrite import RewriteCandidate

class BQMLOptimizationAgent(BaseAgent):
    def __init__(self, generator: CandidateGenerator):
        super().__init__(name="bqml_optimization_agent")
        self.generator = generator

    def run(
        self, 
        sql: str, 
        metadata: dict, 
        ml_context: any = None
    ) -> List[RewriteCandidate]:
        if not sql:
            return []

        return self.generator.generate(
            sql=sql,
            metadata=metadata,
            ml_context=ml_context
        )