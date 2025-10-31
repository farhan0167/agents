import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class EnvConfig:
    """Base class that auto-loads attributes from environment variables"""

    def __init__(self):
        for field_name in self.__annotations__:
            default_value = getattr(self, field_name, None)
            env_value = os.getenv(field_name, default_value)
            setattr(self, field_name, env_value)


class Config(EnvConfig):
    """Configuration class for API settings"""

    API_BASE_URL: str = "http://localhost:8000"

    def get_chat_endpoint(self):
        """Get the chat endpoint URL"""
        return f"{self.API_BASE_URL}/chat"

    def get_history_endpoint(self, thread_id: str):
        """Get the history endpoint URL for a specific thread"""
        return f"{self.API_BASE_URL}/history/{thread_id}"


# Create singleton instance
config = Config()
