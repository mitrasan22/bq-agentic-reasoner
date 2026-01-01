from google.cloud import bigquery
from typing import Dict, Any
import logging


class BQMLMetadataClient:
    """
    Inspects BQML jobs and models safely.
    """

    def __init__(self):
        self.client = bigquery.Client()

    def get_model_metadata(self, model_fqn: str) -> Dict[str, Any]:
        """
        Retrieve metadata about a BQML model.
        Example model_fqn:
          project.dataset.model_name
        """

        model = self.client.get_model(model_fqn)

        return {
            "model_type": model.model_type,
            "training_runs": model.training_runs,
            "creation_time": model.created,
            "expiration_time": model.expires,
            "labels": model.labels,
        }

    def get_model_evaluation(self, model_fqn: str):
        """
        Returns evaluation metadata (no predictions).
        """

        query = f"""
        SELECT *
        FROM ML.EVALUATE(MODEL `{model_fqn}`)
        """

        # SAFE: This is metadata-only ML.EVALUATE
        job = self.client.query(query)
        logging.info(list(job.result()))
        return list(job.result())
