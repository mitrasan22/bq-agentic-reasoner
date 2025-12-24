# BigQuery Audit Log Handler (Cloud Function)

## Purpose
Captures BigQuery audit logs and sends them to the
bq-agentic-reasoner engine for analysis.

## Trigger
Pub/Sub topic connected to Cloud Logging sink.

## Deploy

```bash
gcloud functions deploy handle_bq_audit_log \
  --runtime python311 \
  --trigger-topic bq-audit-logs \
  --region us-central1 \
  --entry-point handle_bq_audit_log \
  --service-account bq-agentic-sa
