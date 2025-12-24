import streamlit as st
import time
from dotenv import load_dotenv
load_dotenv()

st.experimental_set_query_params(ts=str(time.time()))

from ui.services.session_manager import get_session_id
from ui.components.header import render_header
from ui.components.live_feed import render_live_feed
from ui.components.history_view import render_history
from ui.components.filters import render_filters
from ui.components.export import render_export

st.set_page_config(
    page_title="BigQuery Agentic Reasoner",
    layout="wide",
)

def main():
    session_id = get_session_id()

    render_header(session_id)
    filters = render_filters()

    col1, col2 = st.columns([1, 2])

    with col1:
        render_live_feed(session_id, filters)

    with col2:
        render_history(session_id, filters)
        render_export(session_id, filters)


if __name__ == "__main__":
    main()
