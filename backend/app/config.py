"""Application configuration"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://dev:dev_password@localhost:5432/decentralthink_dev"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # JWT
    jwt_secret_key: str = "your-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30 * 24 * 60  # 30 days

    # Third-party APIs
    claude_api_key: str = ""
    stripe_secret_key: str = ""
    stripe_publishable_key: str = ""
    sendgrid_api_key: str = ""
    twitter_api_key: str = ""
    twitter_api_secret: str = ""
    linkedin_access_token: str = ""

    # Application
    environment: str = "development"
    debug: bool = True
    api_v1_prefix: str = "/api/v1"

    # CORS
    allowed_origins: list = ["http://localhost:3000", "http://localhost:8000"]

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()
