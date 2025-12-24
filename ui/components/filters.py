import streamlit as st


def render_filters() -> dict:
    st.sidebar.header("Filters")

    search = st.sidebar.text_input("Search")
    severity = st.sidebar.multiselect(
        "Severity",
        ["LOW", "MEDIUM", "HIGH", "CRITICAL"],
    )

    return {
        "search": search,
        "severity": severity,
    }
