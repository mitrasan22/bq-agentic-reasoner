import streamlit as st
from ui.services.firestore_reader import FirestoreReader


def render_live_feed(session_id: str, filters: dict) -> None:
    st.subheader("Live Feed")

    reader = FirestoreReader()
    runs = reader.fetch_runs(
        session_id=session_id,
        limit=5,
        search=filters.get("search"),
    )

    for run in runs:
        st.markdown(
            f"""
            **{run['job_id']}**
            - Severity: `{run['severity']}`
            - Cost (GB): `{run['estimated_cost_gb']}`
            """
        )
