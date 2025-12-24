from datetime import datetime
from typing import Dict, Any


class EventProcessor:
    """
    Converts raw BigQuery audit log events
    into a normalized internal event format.
    """

    def process(self, raw_event: Dict[str, Any]) -> Dict[str, Any]:
        proto = raw_event.get("protoPayload", {})

        job = (
            proto.get("serviceData", {})
            .get("jobCompletedEvent", {})
            .get("job", {})
        )

        job_cfg = job.get("jobConfiguration", {})
        query_cfg = job_cfg.get("query", {})
        training_cfg = job_cfg.get("training", {})

        stats = (
            job.get("jobStatistics", {})
            .get("query", {})
        )

        job_type = "BQML" if training_cfg else "QUERY"

        return {
            "job_id": job.get("jobName", {}).get("jobId"),
            "timestamp": datetime.utcnow(),
            "job_type": job_type,
            "query": query_cfg.get("query"),
            "metadata": {
                "estimated_bytes": stats.get("totalBytesProcessed", 0),
            },
            "session_id": proto.get("authenticationInfo", {}).get("principalEmail"),
        }
