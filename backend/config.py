from pydantic_settings import BaseSettings
from typing import Optional
import os

# Try to load from environment first, then from .env
os.environ.setdefault("OPENAI_API_KEY", os.environ.get("OPENAI_API_KEY", ""))


class Settings(BaseSettings):
    """Application settings"""
    openai_api_key: Optional[str] = None
    model_name: str = "gpt-3.5-turbo"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    chunk_size: int = 1000
    chunk_overlap: int = 200
    max_documents: int = 50
    faiss_index_path: str = "./data/faiss_index"
    documents_path: str = "./data/documents"

    class Config:
        env_file = "../.env"  # Relative to backend directory
        case_sensitive = False
        extra = "ignore"


settings = Settings()

# Debug: print if API key was loaded
if settings.openai_api_key:
    print(f"✓ OpenAI API key loaded: {settings.openai_api_key[:10]}...")
else:
    print("⚠ Warning: OPENAI_API_KEY not found in environment variables or .env file")
    print(f"  Checked in: ../. env (relative to backend/)")
