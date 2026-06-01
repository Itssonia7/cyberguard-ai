import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(dotenv_path=BASE_DIR / ".env")


class Settings(BaseSettings):
    """Application settings and environment variable validation."""
    GEMINI_API_KEY: str = Field(..., description="API key for the Google Gemini API")
    GEMINI_MODEL: str = Field(default="gemini-2.0-flash", description="The Gemini model to target")
    DEFAULT_TARGET: str = Field(default="127.0.0.1", description="Default target if none provided")
    
    SESSION_MEMORY_DIR: Path = Field(default=BASE_DIR / "sessions", description="Directory for logs")
    REPORT_DIR: Path = Field(default=BASE_DIR / "reports", description="Directory for reports")

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

try:
    settings = Settings()
    settings.SESSION_MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    settings.REPORT_DIR.mkdir(parents=True, exist_ok=True)
except Exception as e:
    print(f"[!] Configuration Error: Ensure you have a .env file configured with GEMINI_API_KEY.\nDetails: {e}")
    raise e