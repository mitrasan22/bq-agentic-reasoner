import streamlit as st
from bq_agentic_reasoner.utils.session import generate_session_id


def get_session_id() -> str:
    if "session_id" not in st.session_state:
        st.session_state["session_id"] = generate_session_id()
    return st.session_state["session_id"]
