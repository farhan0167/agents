import streamlit as st
from sidebar import render_sidebar
from api_client import APIClient


def initialize_session_state():
    """Initialize Streamlit session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "current_thread_id" not in st.session_state:
        st.session_state.current_thread_id = None


def render_chat_messages():
    """Render all chat messages in the conversation"""
    for message in st.session_state.messages:
        role = message.get("role", "user")
        content = message.get("content", "")

        with st.chat_message(role):
            st.markdown(content)


def handle_user_input():
    """Handle user input and stream the response"""
    if prompt := st.chat_input("What would you like to know?"):
        # Add user message to chat
        user_message = {"role": "user", "content": prompt}
        st.session_state.messages.append(user_message)

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response with streaming
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            # Stream the response from the API
            for chunk in APIClient.send_message_stream(
                prompt, st.session_state.current_thread_id
            ):
                full_response += chunk
                message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)

        # Add assistant response to chat history
        assistant_message = {"role": "assistant", "content": full_response}
        st.session_state.messages.append(assistant_message)


def main():
    """Main application entry point"""
    st.set_page_config(
        page_title="Chat Interface",
        page_icon="💬",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Initialize session state
    initialize_session_state()

    # Render sidebar and get current thread
    current_thread_id = render_sidebar()

    # Main chat interface
    st.title("💬 Chat Interface")

    if current_thread_id:
        st.caption(f"Thread ID: {current_thread_id}")
    else:
        st.caption("Start a new conversation")

    # Render existing messages
    render_chat_messages()

    # Handle user input
    handle_user_input()


if __name__ == "__main__":
    main()
