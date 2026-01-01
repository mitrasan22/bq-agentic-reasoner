from bq_agentic_reasoner.models.public import RealtimeResult
from bq_agentic_reasoner.agents.sql_reasoner_agent import SQLIntentAgent
from bq_agentic_reasoner.agents.cost_estimator_agent import CostEstimatorAgent
from bq_agentic_reasoner.agents.risk_agent import RiskAgent
from bq_agentic_reasoner.agents.meta_agent import SeverityAgent
from bq_agentic_reasoner.bigquery.metadata_client import BigQueryMetadataClient
import logging

class RealtimePipeline:
    """
    Executes fast, deterministic analysis immediately
    after job completion.
    """

    def __init__(self):
        self.metadata_client = BigQueryMetadataClient()
        self.intent_agent = SQLIntentAgent()
        self.cost_agent = CostEstimatorAgent()
        self.risk_agent = RiskAgent()
        self.severity_agent = SeverityAgent()

    def run(self, event: dict) -> RealtimeResult:
        logging.info(f"PIPELINE REALTIME EVENT: {event}")
        job_id = event.get("job_id")
        project_id = event.get("metadata", {}).get("project_id")
        actual_metadata = self.metadata_client.get_job_metadata(job_id, project_id)
        intent = self.intent_agent.run(actual_metadata.get("query"))
        cost_gb = self.cost_agent.run(actual_metadata.get("total_bytes_processed", 0))
        total_slots = actual_metadata.get("total_slot_ms", 0)
        risk = self.risk_agent.run(actual_metadata.get("query"),slots=total_slots)

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
            session_id=event.get("user_email"),
        )
