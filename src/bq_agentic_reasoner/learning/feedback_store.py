from datetime import datetime
from google.cloud import firestore

from bq_agentic_reasoner.db.firestore_client import FirestoreClient
from bq_agentic_reasoner.models.rewrite_feedback import RewriteFeedback
from bq_agentic_reasoner.config import load_config


class FeedbackStore:
    """
    Stores rewrite feedback for learning.
    """

    def __init__(self):
        self.db = FirestoreClient.get()
        config = load_config()
        self.collection = config["firestore"]["collections"]["rewrite_feedback"]

    def save(self, feedback: RewriteFeedback) -> None:
        doc = {
            "fingerprint": feedback.fingerprint,
            "optimization_type": feedback.optimization_type,
            "accepted": feedback.accepted,
            "confidence": feedback.confidence,
            "user_id": feedback.user_id,
            "timestamp": feedback.timestamp or datetime.utcnow(),
        }

        self.db.collection(self.collection).add(doc)
