import logging
from typing import Dict, Any

def parse_audit_log_event(raw_log: Dict[str, Any]) -> Dict[str, Any] | None:
    proto = raw_log.get("protoPayload", {})
    
    if proto.get("serviceName") != "bigquery.googleapis.com":
        return None

    method = proto.get("methodName", "")
    if "jobservice.jobcompleted" not in method.lower():
        return None

    service_data = proto.get("serviceData", {})
    job_event = service_data.get("jobCompletedEvent", {}).get("job", {})
    if not job_event:
        return None

    job_name = job_event.get("jobName", {})
    job_id = job_name.get("jobId") or proto.get("resourceName", "").split('/')[-1]
    if not job_id:
        return None

    job_config = job_event.get("jobConfiguration", {})
    query_cfg = job_config.get("query", {})
    
    statement_type = query_cfg.get("statementType", "SELECT")
    job_type = "BQML" if "MODEL" in statement_type or job_config.get("training") else "QUERY"

    stats = job_event.get("jobStatistics", {})
    bytes_processed = stats.get("totalBytesProcessed") or stats.get("query", {}).get("totalBytesProcessed", 0)

    return {
        "job_id": str(job_id),
        "timestamp": raw_log.get("timestamp"),
        "job_type": job_type,
        "query": query_cfg.get("query") or "",
        "statement_type": statement_type,
        "user_email": proto.get("authenticationInfo", {}).get("principalEmail"),
        "metadata": {
            "project_id": job_name.get("projectId")
        }
    }