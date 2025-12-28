from typing import Dict, Any

def parse_audit_log_event(raw_log: Dict[str, Any]) -> Dict[str, Any] | None:
    """
    Extract only completed BigQuery QUERY / BQML jobs.
    """
    proto = raw_log.get("protoPayload", {})
    service = proto.get("serviceName")

    if service != "bigquery.googleapis.com":
        return None

    method = proto.get("methodName", "")
    if "jobservice.jobcompleted" not in method.lower():
        return None

    # --- FIX: Robust Job ID Extraction ---
    # Try resourceName first (e.g., "projects/my-id/jobs/job_ASDF123")
    resource_name = proto.get("resourceName", "")
    job_id = resource_name.split('/')[-1] if 'jobs/' in resource_name else None

    job_event = (
        proto.get("serviceData", {})
        .get("jobCompletedEvent", {})
        .get("job", {})
    )

    if not job_event:
        return None

    # Fallback for job_id if resourceName didn't work
    if not job_id:
        job_id = job_event.get("jobName", {}).get("jobId")
    
    # If job_id is STILL None, we must return to prevent Pydantic crash
    if not job_id:
        return None

    job_config = job_event.get("jobConfiguration", {})
    query_cfg = job_config.get("query", {})
    training_cfg = job_config.get("training") # Kept your BQML logic

    job_type = "BQML" if training_cfg else "QUERY"

    stats = (
        job_event.get("jobStatistics", {})
        .get("query", {})
    )

    return {
        "job_id": job_id,
        "timestamp": raw_log.get("timestamp"),
        "job_type": job_type,
        "query": query_cfg.get("query") or "", # Ensure string, not None
        "metadata": {
            "estimated_bytes": stats.get("totalBytesProcessed", 0),
        },
        "session_id": proto.get("authenticationInfo", {}).get("principalEmail"),
    }