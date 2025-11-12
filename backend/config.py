"""
FastAPI Backend Configuration
==============================
Centralized configuration management using Pydantic Settings
"""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings with environment variable support"""

    # App settings
    app_name: str = "Healthcare AI Agent API"
    app_version: str = "1.0.0"
    debug: bool = False

    # API settings
    api_prefix: str = "/api"

    # CORS settings
    cors_origins: List[str] = [
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # Alternative React port
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]

    # OpenAI settings
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    openai_temperature: float = 0.3

    # HuggingFace settings
    huggingface_api_key: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
