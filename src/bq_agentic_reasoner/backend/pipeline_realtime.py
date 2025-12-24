from bq_agentic_reasoner.models.public import RealtimeResult
from bq_agentic_reasoner.agents.sql_reasoner_agent import SQLIntentAgent
from bq_agentic_reasoner.agents.cost_estimator_agent import CostEstimatorAgent
from bq_agentic_reasoner.agents.risk_agent import RiskAgent
from bq_agentic_reasoner.agents.meta_agent import SeverityAgent


class RealtimePipeline:
    """
    Executes fast, deterministic analysis immediately
    after job completion.
    """

    def __init__(self):
        self.intent_agent = SQLIntentAgent()
        self.cost_agent = CostEstimatorAgent()
        self.risk_agent = RiskAgent()
        self.severity_agent = SeverityAgent()

    def run(self, event: dict) -> RealtimeResult:
        intent = self.intent_agent.run(event.get("query"))
        cost_gb = self.cost_agent.run(
            event["metadata"].get("estimated_bytes", 0)
        )
        risk = self.risk_agent.run(event.get("query"))

        severity = self.severity_agent.run(
            cost_gb=cost_gb,
            risk=risk,
            intent=intent,
        )

        return RealtimeResult(
            job_id=event["job_id"],
            timestamp=event["timestamp"],
            job_type=event["job_type"],
            severity=severity,
            intent=intent,
            estimated_cost_gb=cost_gb,
            risk=risk,
            session_id=event.get("session_id"),
        )
