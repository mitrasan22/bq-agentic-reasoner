import streamlit as st


def render_rewrite(run: dict) -> None:
    rewrite = run.get("rewrite_set")
    if not rewrite:
        return

    st.subheader("Optimized Queries")

    for candidate in rewrite.get("candidates", []):
        st.code(candidate["optimized_query"], language="sql")
        st.caption(candidate["explanation"])
