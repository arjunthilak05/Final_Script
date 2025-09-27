from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # Database Configuration
    database_url: str = "postgresql://username:password@localhost:5432/your_database"
    redis_url: str = "redis://localhost:6379/0"
    
    # Pinecone Configuration
    pinecone_api_key: str = ""
    pinecone_environment: str = ""
    pinecone_index_name: str = ""
    
    # OpenAI Configuration
    openai_api_key: str = ""
    
    
    # OpenRouter Configuration
    openrouter_api_key: str = ""
    
    # FastAPI Configuration
    secret_key: str = "your-secret-key-change-this-in-production"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000
    
    # LangSmith Configuration (optional)
    langchain_tracing_v2: bool = False
    langchain_api_key: Optional[str] = None
    langchain_project: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
