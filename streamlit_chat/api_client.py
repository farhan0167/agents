import requests
from typing import Dict, List, Any, Iterator
from config import config


class APIClient:
    """Client for interacting with the chat API"""

    @staticmethod
    def get_thread_history(thread_id: str) -> List[Dict[str, Any]]:
        """
        Fetch chat history for a specific thread.

        Args:
            thread_id: The thread ID to fetch history for

        Returns:
            List of message dictionaries
        """
        try:
            url = config.get_history_endpoint(thread_id)
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching thread history: {e}")
            return []

    @staticmethod
    def send_message_stream(
        user_message: str, thread_id: str = None
    ) -> Iterator[str]:
        """
        Send a message to the chat API and stream the response.

        Args:
            user_message: The user's message to send
            thread_id: Optional thread ID for continuing a conversation

        Yields:
            Chunks of the streamed response
        """
        try:
            url = config.get_chat_endpoint()
            payload = {"user_message": user_message}

            if thread_id:
                payload["thread_id"] = thread_id

            response = requests.post(url, json=payload, stream=True)
            response.raise_for_status()

            # Stream the response
            for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                if chunk:
                    yield chunk

        except requests.exceptions.RequestException as e:
            yield f"Error: {str(e)}"

    @staticmethod
    def get_threads() -> List[Dict[str, Any]]:
        """
        Fetch list of all available threads.

        Note: This endpoint might need to be implemented on the API side.
        Returns an empty list if not available.

        Returns:
            List of thread dictionaries with 'id' and 'title' keys
        """
        try:
            url = f"{config.API_BASE_URL}/threads"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching threads: {e}")
            return []
