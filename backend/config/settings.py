from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    APP_NAME: str = "PAISA // Enterprise Agent Platform"
    DEBUG: bool = False
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]
    
    DATABASE_URL: str = "sqlite+aiosqlite:///./pine.db"
    
    # ── Google Gemini / Vertex AI (Primary — Track B) ──────────────────────────
    GOOGLE_API_KEY: str = ""                        # Gemini API key
    GOOGLE_CLOUD_PROJECT: str = ""                  # GCP project ID
    GOOGLE_CLOUD_LOCATION: str = "us-central1"      # Vertex AI region
    GEMINI_MODEL: str = "gemini-2.0-flash"           # Fast model for routing

    # ── AWS Credentials (Legacy Fallback) ──────────────────────────────────────
    AWS_REGION: str = "us-east-1"
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_SESSION_TOKEN: Optional[str] = None
    BEDROCK_MODEL_ID: str = "amazon.nova-lite-v1:0"
    
    # ── Pine Labs ──────────────────────────────────────────────────────────────
    PINE_LABS_BASE_URL: str = "https://api.pluralonline.com"
    PINE_LABS_MERCHANT_ID: str = "121562"
    PINE_LABS_MID: str = "121562"
    PINE_LABS_API_KEY: str = ""
    PINE_LABS_CLIENT_ID: str = ""
    PINE_LABS_CLIENT_SECRET: str = ""

    # ── Groq AI (Legacy Fallback) ──────────────────────────────────────────────
    GROQ_API_KEY: str = ""

    # ── Nasiko Control Plane ───────────────────────────────────────────────────
    NASIKO_ENABLED: bool = True
    NASIKO_BASE_URL: str = "http://localhost:8080"

    class Config:
        env_file = ".env"

settings = Settings()

