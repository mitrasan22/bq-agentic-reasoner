from google.cloud import bigquery
from typing import Dict, Any
import logging
import time

class BQMLMetadataClient:
    """
    Inspects BQML jobs and models safely.
    """

    def __init__(self):
        self.client = bigquery.Client()

    def get_model_metadata(self, model_fqn: str) -> Dict[str, Any]:
        """
        Retrieve metadata about a BQML model.
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
        Returns evaluation metadata (no predictions) with simple retry logic.
        """
        query = f"""
        SELECT *
        FROM ML.EVALUATE(MODEL `{model_fqn}`)
        """

        for attempt in range(3):
            try:
                job = self.client.query(query)
                results = list(job.result())
                if results:
                    logging.info(f"ML stats found: {results}")
                    return results
            except Exception as e:
                logging.warning(f"Attempt {attempt + 1} failed to fetch ML stats: {e}")

            if attempt < 2:
                time.sleep(2 * (attempt + 1))

        return []