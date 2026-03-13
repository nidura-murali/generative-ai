
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal

class Settings(BaseSettings):
    # Environment name
    ENV: Literal["local", "dev", "qa", "prod"] = "local"

    # App metadata
    APP_NAME: str = "My FastAPI Service"
    VERSION: str = "1.0.0"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = False

    # Security / integrations
    # JWT_SECRET: str = "CHANGE_ME"
    # DATABASE_URL: str
    SBCA_HOST: str

    model_config = SettingsConfigDict(
        env_file=".env",              # optional .env for local dev
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

# Singleton accessor (lazy load once per process)
_settings: Settings | None = None

def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()  # reads env vars / .env
    return _settings
