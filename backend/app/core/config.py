from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # App
    APP_NAME: str = "Resume Optimizer API"
    ENVIRONMENT: str = "development"
    CORS_ORIGINS: str = "http://localhost:5173"

    # Database
    DATABASE_URL: str = "postgresql+psycopg://postgres:postgres@localhost:5433/resume_optimizer"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # AWS S3
    AWS_REGION: str = "us-east-1"
    S3_BUCKET: str = "resumer-optimizer-dev"
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""

    # Gemini
    GEMINI_API_KEY: str = ""
    EMBEDDING_MODEL: str = "gemini-embedding-001"
    EMBEDDING_DIMENSIONS: int = 1536
    LLM_MODEL: str = "gemini-flash-latest"

    # Uploads
    MAX_UPLOAD_MB: int = 10

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

@lru_cache
def get_settings() -> Settings:
    return Settings()