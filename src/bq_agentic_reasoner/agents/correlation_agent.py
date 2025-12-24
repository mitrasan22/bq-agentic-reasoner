from bq_agentic_reasoner.agents.base import BaseAgent


class CorrelationAgent(BaseAgent):
    """
    Detects anomalous cost spikes relative to history.
    """

    def __init__(self):
        super().__init__(name="correlation_agent")

    def run(self, current_cost: float, historical_costs: list[float]) -> bool:
        if not historical_costs:
            return False

        avg = sum(historical_costs) / len(historical_costs)
        return current_cost > (avg * 2)
