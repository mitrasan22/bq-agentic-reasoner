import base64
import json
import logging
import sys
from typing import Dict, Any
from bq_agentic_reasoner import Orchestrator
from parser import parse_audit_log_event

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

def handle_bq_audit_log(event: Dict[str, Any], context) -> None:
    if "data" not in event:
        return
    
    logging.info("🔥 Function triggered")
    
    try:
        payload = base64.b64decode(event["data"]).decode("utf-8")
        raw_log = json.loads(payload)

        parsed_event = parse_audit_log_event(raw_log)
        logging.info(f"Parsed Event: {parsed_event}")
        
        if not parsed_event:
            logging.info("Log ignored: Not a BQ Job Completion event.")
            return

        orchestrator = Orchestrator()
        orchestrator.handle_event(parsed_event)
        
    except Exception as e:
        logging.error(f"Function failed: {str(e)}", exc_info=True)
        raise e