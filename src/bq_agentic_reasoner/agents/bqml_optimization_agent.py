from bq_agentic_reasoner.agents.base import BaseAgent
from bq_agentic_reasoner.rewrite.candidate_generator import CandidateGenerator


class BQMLOptimizationAgent(BaseAgent):
    """
    Generates optimization candidates for BQML statements.
    """

    def __init__(self, generator: CandidateGenerator):
        super().__init__(name="bqml_optimization_agent")
        self.generator = generator

    def run(self, *, sql: str, metadata: dict):
        if not sql:
            return []
        return self.generator.generate(sql=sql, metadata=metadata)
