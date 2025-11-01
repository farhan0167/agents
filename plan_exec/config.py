from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Config(BaseSettings):
    OPENAI_API_KEY: str
    TAVILY_API_KEY: str
    PHOENIX_COLLECTOR_ENDPOINT: str = "http://localhost:4317"
    
    
config = Config()