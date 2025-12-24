from google.cloud import bigquery
from typing import Dict, Any, Optional


class BigQueryMetadataClient:
    """
    Read-only BigQuery metadata client.
    """

    def __init__(self):
        self.client = bigquery.Client()

    def get_job_metadata(self, job_id: str, project_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Fetch metadata for a completed BigQuery job.
        """

        job = self.client.get_job(job_id, project=project_id)

        metadata = {
            "job_id": job.job_id,
            "job_type": job.job_type,
            "state": job.state,
            "created": job.created,
            "started": job.started,
            "ended": job.ended,
            "total_bytes_processed": getattr(job, "total_bytes_processed", 0),
            "total_slot_ms": getattr(job, "total_slot_ms", 0),
            "user_email": getattr(job, "user_email", None),
        }

        if hasattr(job, "query"):
            metadata["query"] = job.query

        return metadata
