from langchain_openai import OpenAI
from langchain.chat_models import init_chat_model

from config import config



llm = init_chat_model(
    "openai:gpt-4o",
    temperature=0
)
