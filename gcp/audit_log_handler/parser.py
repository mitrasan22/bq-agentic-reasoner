from typing import Dict, Any
import logging

def parse_audit_log_event(raw_log: Dict[str, Any]) -> Dict[str, Any] | None:
    """
    Extract only completed BigQuery QUERY / BQML jobs.
    """
    logging.info(f"Raw Log: {raw_log}")
    proto = raw_log.get("protoPayload", {})
    service = proto.get("serviceName")
    if service != "bigquery.googleapis.com":
        return None

    method = proto.get("methodName", "")
    if "jobservice.jobcompleted" not in method.lower():
        return None

    service_data = proto.get("serviceData", {})
    job_completed_event = service_data.get("jobCompletedEvent", {})
    job_event = job_completed_event.get("job", {})

    if not job_event:
        return None

    job_id = job_event.get("jobName", {}).get("jobId")

    if not job_id:
        resource_name = proto.get("resourceName", "")
        job_id = resource_name.split('/')[-1] if 'jobs/' in resource_name else None

    if not job_id:
        logging.warning("No Job ID found even though job is completed.")
        return None

    job_config = job_event.get("jobConfiguration", {})
    query_cfg = job_config.get("query", {})
    training_cfg = job_config.get("training")

    job_type = "BQML" if training_cfg else "QUERY"

    # 6. FIX: Get Statistics
    # In your raw JSON, totalBytesProcessed is directly in jobStatistics
    stats = job_event.get("jobStatistics", {})
    
    # Check if it's nested in .query or at the top level of stats
    bytes_processed = stats.get("totalBytesProcessed")
    if bytes_processed is None:
        bytes_processed = stats.get("query", {}).get("totalBytesProcessed", 0)

    return {
        "job_id": str(job_id),
        "timestamp": raw_log.get("timestamp"),
        "job_type": job_type,
        "query": query_cfg.get("query") or "",
        "metadata": {
            "estimated_bytes": int(bytes_processed),
        },
        "session_id": proto.get("authenticationInfo", {}).get("principalEmail"),
    }