import base64
import json
from typing import Dict, Any

from bq_agentic_reasoner import Orchestrator
from parser import parse_audit_log_event

def handle_bq_audit_log(event: Dict[str, Any], context) -> None:
    """
    Cloud Function entry point.
    Triggered by BigQuery audit log events via Pub/Sub.
    """

    if "data" not in event:
        return

    payload = base64.b64decode(event["data"]).decode("utf-8")
    raw_log = json.loads(payload)

    parsed_event = parse_audit_log_event(raw_log)
    orchestrator = Orchestrator()
    if not parsed_event:
        return

    orchestrator.handle_event(parsed_event)
