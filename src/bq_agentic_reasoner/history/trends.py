from typing import List
from google.cloud import firestore

from bq_agentic_reasoner.config import load_config


def load_recent_costs(
    *,
    session_id: str | None,
    limit: int = 20,
) -> List[float]:
    """
    Load recent cost history for a session.
    """

    config = load_config()
    collection_name = config["firestore"]["collections"]["runs"]

    db = firestore.Client()

    query = (
        db.collection(collection_name)
        .order_by("timestamp", direction=firestore.Query.DESCENDING)
        .limit(limit)
    )

    if session_id:
        query = query.where("session_id", "==", session_id)

    docs = query.stream()

    return [
        doc.to_dict().get("estimated_cost_gb", 0.0)
        for doc in docs
    ]
