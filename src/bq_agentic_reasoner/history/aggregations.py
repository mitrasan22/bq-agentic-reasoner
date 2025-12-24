from typing import Dict
from google.cloud import firestore

from bq_agentic_reasoner.config import load_config


def aggregate_by_severity(
    *,
    session_id: str | None = None,
) -> Dict[str, int]:
    """
    Count runs by severity level.
    """

    config = load_config()
    collection_name = config["firestore"]["collections"]["runs"]

    db = firestore.Client()

    query = db.collection(collection_name)
    if session_id:
        query = query.where("session_id", "==", session_id)

    counts = {
        "LOW": 0,
        "MEDIUM": 0,
        "HIGH": 0,
        "CRITICAL": 0,
    }

    for doc in query.stream():
        sev = doc.to_dict().get("severity")
        if sev in counts:
            counts[sev] += 1

    return counts
