from typing import List, Dict
from google.cloud import firestore

from bq_agentic_reasoner.config import load_config
from bq_agentic_reasoner.db.firestore_client import FirestoreClient


class FirestoreReader:
    """
    Read-only Firestore access for UI.
    """

    def __init__(self):
        self.db = FirestoreClient.get()
        config = load_config()
        self.collection = config["firestore"]["collections"]["runs"]

    def fetch_runs(
        self,
        *,
        session_id: str,
        limit: int = 20,
        search: str | None = None,
        cursor=None,
    ) -> List[Dict]:
        query = (
            self.db.collection(self.collection)
            .where("session_id", "==", session_id)
            .order_by("timestamp", direction=firestore.Query.DESCENDING)
            .limit(limit)
        )

        if cursor:
            query = query.start_after(cursor)

        docs = list(query.stream())

        results = []
        for doc in docs:
            data = doc.to_dict()
            data["_cursor"] = doc
            if search:
                if search.lower() not in str(data).lower():
                    continue
            results.append(data)

        return results
