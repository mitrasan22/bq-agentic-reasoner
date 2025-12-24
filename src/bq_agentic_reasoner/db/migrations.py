"""
Firestore migration hooks.

Currently no-op.
Used when schemas evolve.
"""

from google.cloud import firestore
from bq_agentic_reasoner.db.firestore_client import FirestoreClient


def run_migrations() -> None:
    """
    Apply Firestore migrations if needed.
    Currently a no-op.
    """

    db = FirestoreClient.get()

    # Example placeholder:
    # - add new field
    # - backfill missing values
    # - rename fields

    return
