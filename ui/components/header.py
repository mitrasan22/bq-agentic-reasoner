import streamlit as st


def render_header(session_id: str) -> None:
    st.title("🧠 BigQuery Agentic Reasoner")
    st.caption(f"Session: `{session_id}`")
