import base64
import json
import logging
import sys
from typing import Dict, Any
from bq_agentic_reasoner.backend.orchestrator import Orchestrator
from parser import parse_audit_log_event

root = logging.getLogger()
if root.handlers:
    for handler in root.handlers:
        root.removeHandler(handler)

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s:%(name)s:%(message)s',
    stream=sys.stdout
)

orchestrator = Orchestrator()

def handle_bq_audit_log(event: Dict[str, Any], context) -> None:
    if "data" not in event:
        return
    
    try:
        payload = base64.b64decode(event["data"]).decode("utf-8")
        raw_log = json.loads(payload)

        parsed_event = parse_audit_log_event(raw_log)
        
        if not parsed_event:
            return

        if "bq-agentic-reasoner" in parsed_event.get("user_email", ""):
            return

        orchestrator.handle_event(parsed_event)
        
    except Exception as e:
        logging.error(f"Function failed: {str(e)}", exc_info=True)