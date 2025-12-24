import streamlit as st
from ui.services.firestore_reader import FirestoreReader


def render_history(session_id: str, filters: dict) -> None:
    st.subheader("History")

    reader = FirestoreReader()
    runs = reader.fetch_runs(
        session_id=session_id,
        limit=20,
        search=filters.get("search"),
    )

    for run in runs:
        with st.expander(f"Job {run['job_id']}"):
            st.json(run)
