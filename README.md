# BQ-Agentic-Reasoner

## Overview
BQ-Agentic-Reasoner is an advanced system for reasoning, optimizing, and monitoring BigQuery queries. It leverages agentic principles to enhance query performance, reduce costs, and provide insights into query behavior.

## Features
- **Query Optimization**: Automatically optimize BigQuery queries for better performance and lower costs.
- **Cost Estimation**: Estimate query costs before execution.
- **Risk Analysis**: Identify potential risks in query execution.
- **Learning and Feedback**: Incorporates learning mechanisms to improve over time based on feedback.
- **Integration with Firestore**: Stores and retrieves metadata and configurations using Google Firestore.
- **Streamlit UI**: Provides an interactive user interface for monitoring and managing queries.

## Project Structure
```
|
├── gcp/                       # Google Cloud Platform utilities
│   ├── audit_log_handler/     # Main cloudfunction
├── src/                       # Source code
│   ├── bq_agentic_reasoner/   # Core library
│   │   ├── agents/            # Query agents (optimization, risk, etc.)
│   │   ├── backend/           # Backend orchestration and pipelines
│   │   ├── bigquery/          # BigQuery client utilities
│   │   ├── config/            # Configuration files (YAML)
│   │   ├── db/                # Database clients and schemas
│   │   ├── history/           # Query history and trends
│   │   ├── learning/          # Learning and feedback mechanisms
│   │   ├── llm/               # Large Language Model utilities
│   │   ├── models/            # Data models
│   │   ├── rewrite/           # Query rewrite components
│   │   ├── schemas/           # JSON schemas for data validation
│   │   ├── security/          # Security modules
│   │   ├── utils/             # Utility functions
├── ui/                        # Streamlit-based user interface
│   ├── components/            # UI components
│   ├── services/              # Backend services for the UI
│   ├── assets/                # Static assets (CSS, images, etc.)
├── pyproject.toml             # Project metadata and dependencies
├── requirements.txt           # Additional Python dependencies
```

## Installation

### Prerequisites
- Python 3.10 or higher
- Google Cloud SDK

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/mitrasan22/bq-agentic-reasoner.git
   cd bq-agentic-reasoner
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Install development dependencies (optional):
   ```bash
   pip install -e .[dev]
   ```

## Usage

## Configuration
Configuration files are located in `src/bq_agentic_reasoner/config/`. Update the YAML files to customize thresholds, security settings, and other parameters.

## Deployment

### Deploying the GCP Cloud Function
The `gcp/audit_log_handler` directory contains a Cloud Function for handling BigQuery audit logs. Follow these steps to deploy it:

1. Ensure you have the Google Cloud SDK installed and authenticated.
2. Navigate to the `gcp/audit_log_handler` directory:
   ```bash
   cd gcp/audit_log_handler
   ```
3. Deploy the Cloud Function using the following command:
   ```bash
   gcloud functions deploy handle_bq_audit_log \
     --runtime python311 \
     --trigger-topic bq-audit-logs \
     --region us-central1 \
     --entry-point handle_bq_audit_log \
     --service-account <service-account>
   ```

### Running Queries in BigQuery UI
To run queries in the BigQuery UI:

1. Open the [Google Cloud Console BigQuery page](https://console.cloud.google.com/bigquery).
2. Select your project from the project dropdown.
3. Navigate to the `SQL Workspace`.
4. Write your SQL query in the editor.
5. Click the `Run` button to execute the query.
6. View the results in the `Query Results` pane.

### Running the Streamlit App to monitor query
To launch the Streamlit-based user interface:
```bash
streamlit run ui/streamlit_app.py
```
<img width="1919" height="914" alt="image" src="https://github.com/user-attachments/assets/9b64f868-8951-490a-ab2f-0a77a29e63c2" />

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request.

## License
This project is licensed under the MIT License.

## Authors
- Santanu Mitra
