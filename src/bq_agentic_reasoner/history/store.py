from typing import Union
from datetime import datetime
import logging

from google.cloud import firestore
from bq_agentic_reasoner.db.firestore_client import FirestoreClient
from bq_agentic_reasoner.models.public import RealtimeResult, RunResult
from bq_agentic_reasoner.config import load_config


def record_run(result: Union[RealtimeResult, RunResult]) -> None:
    """
    Persist a run result to Firestore.

    This function is intentionally simple and synchronous.
    """

    config = load_config()
    collection_name = config["firestore"]["collections"]["runs"]

    db = FirestoreClient.get()
    logging.info(f"Recording run result to Firestore db: {db}")

    doc = {
        "job_id": result.job_id,
        "timestamp": result.timestamp,
        "job_type": result.job_type,
        "severity": result.severity,
        "intent": result.intent,
        "estimated_cost_gb": result.estimated_cost_gb,
        "risk": result.risk,
        "session_id": result.session_id,
        "status": result.status,
        "created_at": datetime.utcnow(),
    }

    # Optional enrichment fields
    if hasattr(result, "recommendation") and result.recommendation:
        doc["recommendation"] = result.recommendation.dict()

    if hasattr(result, "rewrite_set") and result.rewrite_set:
        doc["rewrite_set"] = result.rewrite_set.dict()

    db.collection(collection_name).document(result.job_id).set(doc)
    print(doc.keys())
