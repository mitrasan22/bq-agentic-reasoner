import streamlit as st
import pandas as pd
from ui.services.firestore_reader import FirestoreReader


def render_export(session_id: str, filters: dict):
    st.subheader("Export")

    reader = FirestoreReader()
    runs = reader.fetch_runs(
        session_id=session_id,
        limit=100,
        search=filters.get("search"),
    )

    if not runs:
        return

    df = pd.DataFrame(runs)
    st.download_button(
        label="Download CSV",
        data=df.to_csv(index=False),
        file_name="bq_agentic_report.csv",
        mime="text/csv",
    )
