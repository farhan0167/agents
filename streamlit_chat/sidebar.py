import streamlit as st
from api_client import APIClient


def render_sidebar():
    """
    Render the sidebar with thread list.

    Returns:
        The selected thread ID or None
    """
    with st.sidebar:
        st.title("Chat Threads")

        # Button to create a new thread
        if st.button("+ New Chat", use_container_width=True):
            st.session_state.current_thread_id = None
            st.session_state.messages = []
            st.rerun()

        st.divider()

        # Fetch and display threads
        threads = APIClient.get_threads()

        if not threads:
            st.info("No threads available. Start a new chat!")
        else:
            # Display threads as buttons
            for thread in threads:
                thread_id = thread.get("id", "")
                thread_title = thread.get("title", f"Thread {thread_id[:8]}...")

                # Highlight the current thread
                is_current = st.session_state.get("current_thread_id") == thread_id

                if st.button(
                    thread_title,
                    key=f"thread_{thread_id}",
                    use_container_width=True,
                    type="primary" if is_current else "secondary",
                ):
                    # Load thread history when clicked
                    st.session_state.current_thread_id = thread_id
                    st.session_state.messages = APIClient.get_thread_history(thread_id)
                    st.rerun()

        st.divider()

        # Display API configuration
        with st.expander("Settings"):
            st.caption("API Configuration")
            from config import config

            st.code(f"API Base URL: {config.API_BASE_URL}")

    return st.session_state.get("current_thread_id")
