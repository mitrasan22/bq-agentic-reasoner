from datetime import datetime
from typing import Dict, Any
import logging

class EventProcessor:
    def process(self, raw_event: Dict[str, Any]) -> Dict[str, Any]:
        # --- FIX: Check if we are receiving an already-parsed event ---
        if "job_id" in raw_event:
            logging.info(f"Processor: Received pre-parsed event for {raw_event['job_id']}")
            # Ensure timestamp is a datetime object for Pydantic
            if isinstance(raw_event.get("timestamp"), str):
                try:
                    raw_event["timestamp"] = datetime.fromisoformat(raw_event["timestamp"].replace("Z", "+00:00"))
                except:
                    raw_event["timestamp"] = datetime.utcnow()
            return raw_event

        # --- Handle Raw Audit Log ---
        proto = raw_event.get("protoPayload", {})
        job = proto.get("serviceData", {}).get("jobCompletedEvent", {}).get("job", {})

        job_id = job.get("jobName", {}).get("jobId")
        # Fallback if the path is slightly different
        if not job_id:
            resource_name = proto.get("resourceName", "")
            job_id = resource_name.split('/')[-1] if 'jobs/' in resource_name else None

        job_cfg = job.get("jobConfiguration", {})
        query_cfg = job_cfg.get("query", {})
        training_cfg = job_cfg.get("training", {})

        stats = job.get("jobStatistics", {}).get("query", {})
        bytes_processed = stats.get("totalBytesProcessed") or job.get("jobStatistics", {}).get("totalBytesProcessed", 0)

        return {
            "job_id": job_id,
            "timestamp": datetime.utcnow(),
            "job_type": "BQML" if training_cfg else "QUERY",
            "query": query_cfg.get("query") or "",
            "metadata": {
                "estimated_bytes": bytes_processed,
            },
            "session_id": proto.get("authenticationInfo", {}).get("principalEmail"),
        }