import streamlit as st


def render_feedback(run_id: str):
    st.radio(
        "Was this helpful?",
        ["Yes", "No"],
        key=f"feedback_{run_id}",
    )
