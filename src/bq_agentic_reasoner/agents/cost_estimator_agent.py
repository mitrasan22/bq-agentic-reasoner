from bq_agentic_reasoner.agents.base import BaseAgent


class CostEstimatorAgent(BaseAgent):
    """
    Estimates BigQuery scan cost in GB.
    """

    def __init__(self):
        super().__init__(name="cost_estimator_agent")

    def run(self, total_bytes: int) -> float:
        if not total_bytes or total_bytes < 0:
            return 0.0
        return round(total_bytes / (1024 ** 3), 3)
